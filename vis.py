import pyglet
from pyglet import shapes
import math
from secondOrderDE import second_order_DE_nonlinear
from secondOrderDE import second_order_DE_nonlinear_rk4
from secondOrderDE import second_order_DE_nonlinear_rk4_one_step
from pathlib import Path
from secondOrderDE import nick_test
from datetime import datetime
import numpy as np
import physics


#### Nick has to implement his changes from his backup --> making the init more user friendly and fixing up the old comments
# make planes scaleable with worldscale



# --- Aircraft Visualizer ---
class AircraftVisualizer(pyglet.window.Window):
    def __init__(self):
        # Initialize physics variables
        physics.globalize_physics_vars(dihedral=-3, Mass=1000, WingLength=4, WingWidth=1, BodyArea=5,
                                       cLift_a0=0.25, cL_slope=0.2,
                                       altitude=1000, cruise=52, I_roll=1000, drag_mult = 1)
        
        self.aircraft_angle = 5.0  # degrees
        self.worldscale = 10.0  # zoom level
        

        # --- Constants ---
        global WINDOW_WIDTH
        global WINDOW_HEIGHT
        WINDOW_WIDTH = 1000
        WINDOW_HEIGHT = 700
        self.VIEWPORT_MARGIN = 100  # pixels from edge before camera moves

        global NUM_OF_FRAMES
        global SIM_TIME
        NUM_OF_FRAMES = 60
        SIM_TIME = 20 
        # Background image
        # https://unsplash.com/photos/sky-cloud-blue-background-paronama-web-cloudy-summer-winter-season-day-light-beauty-horizon-spring-brigth-gradient-calm-abstract-backdrop-air-nature-view-wallpaper-landscape-cyan-color-environment-wkVWKgeyEEs
        # 3000x1097
        global pic_width
        global pic_height
        pic_width = 3000
        pic_height = 1097


        # Aircraft init state
        # NOTE: COORDNIATES LOAD FROM BOTTOM LEFT
        # (0,0) is bottom-left of background image

        self.aircraft_x = pic_width/2
        self.aircraft_y = pic_height - WINDOW_HEIGHT/2
        self.initx = self.aircraft_x
        self.inity = self.aircraft_y
        
        self.aircraft_dx = 0.0
        self.aircraft_dy = 0.0
        self.aircraft_dangle = 0.0


        # Load aircraft sprite
        if physics.dihedral < 0:
            sprite_file = "mirage.png"
        elif physics.dihedral > 0:
            sprite_file = "777.png"
        else:
            sprite_file = "su27.png"

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Aircraft Visualizer - Pyglet 2.x")
        pyglet.gl.glClearColor(0.53, 0.81, 0.98, 1.0)  # Sky blue background

        self.aircraft_image = pyglet.image.load(sprite_file)
        self.aircraft_image.anchor_x = self.aircraft_image.width // 2
        self.aircraft_image.anchor_y = self.aircraft_image.height // 2
        self.aircraft_sprite = pyglet.sprite.Sprite(
            img=self.aircraft_image,
            x=0,
            y=0
        )
        self.aircraft_sprite.scale = self.worldscale / 20  # Scale down the aircraft sprite


        # Camera init pos (defining top-left corner)
        self.cam_x = pic_width/2 - WINDOW_WIDTH / 2
        self.cam_y = pic_height
        
        # store flight data

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # remove problematic characters
        self.data_path_name = Path("data") / f"data-{timestamp}.txt"

        # HUD labels
        self.label_pos = pyglet.text.Label('', x=10, y=WINDOW_HEIGHT-30)
        self.label_pitch = pyglet.text.Label('', x=10, y=WINDOW_HEIGHT-60)


        
        # 60 FPS
        pyglet.clock.schedule_interval(self.update, float(1/NUM_OF_FRAMES))

        # Load background image
        self.background_img = pyglet.image.load("background.jpeg")
        self.background_img.anchor_x = 0
        self.background_img.anchor_y = 0
        self.runtime = 0.0


        # load init plot coords
        self.plot_coordy = self.aircraft_y - self.cam_x # not right coody is a relative aircraft is a global
        self.plot_coordx = self.aircraft_x  - self.cam_y
        self.scaled_aircraft_x = self.plot_coordx + self.cam_x
        self.scaled_aircraft_y = self.plot_coordy + self.cam_y
        print("\nRunning  .  .  . \n")

        


    def camera(self):
        # Camera 
        left_edge = self.cam_x + self.VIEWPORT_MARGIN
        right_edge = self.cam_x + WINDOW_WIDTH - self.VIEWPORT_MARGIN
        bottom_edge = self.cam_y + self.VIEWPORT_MARGIN
        top_edge = self.cam_y + WINDOW_HEIGHT - self.VIEWPORT_MARGIN


        if (self.scaled_aircraft_x) < left_edge:
            self.cam_x = self.scaled_aircraft_x - self.VIEWPORT_MARGIN
        elif self.scaled_aircraft_x > right_edge:
            self.cam_x = self.scaled_aircraft_x - WINDOW_WIDTH + self.VIEWPORT_MARGIN

        if self.scaled_aircraft_y < bottom_edge:
            self.cam_y = self.scaled_aircraft_y - self.VIEWPORT_MARGIN
        elif self.scaled_aircraft_y > top_edge:
            self.cam_y = self.scaled_aircraft_y - WINDOW_HEIGHT + self.VIEWPORT_MARGIN

        # Clamp camera to world
        return (max(0, min(self.cam_x, pic_width - WINDOW_WIDTH)), max(0, min(self.cam_y, pic_height - WINDOW_HEIGHT)))

    def update(self, dt):
        self.runtime += dt
        
        # --- Calculate new aircraft properties from previous using RK 4 solver ---
        self.x1, self.y1, self.bank1, self.dx1, self.dy1, self.dbank1 = second_order_DE_nonlinear_rk4_one_step(self.aircraft_x, self.aircraft_y, self.aircraft_angle, 
                                                                                                               self.aircraft_dx, self.aircraft_dy, self.aircraft_dangle, 
                                                                                                               1/NUM_OF_FRAMES)

        # Update positions       
        self.aircraft_x = self.x1
        self.aircraft_y = self.y1
        self.aircraft_angle = self.bank1

        # Update velocities
        self.aircraft_dx = self.dx1
        self.aircraft_dy = self.dy1
        self.aircraft_dangle = self.dbank1

        # Check failure conditions
        self.scaled_aircraft_x = self.plot_coordx + self.cam_x
        self.scaled_aircraft_y = self.plot_coordy + self.cam_y

        if (self.scaled_aircraft_y < 0) or (self.scaled_aircraft_y > pic_height) or (self.scaled_aircraft_x < 0) or (self.scaled_aircraft_x > pic_width):
            print("Aircraft has left the world boundaries. Simulation ending.")
            pyglet.app.exit()
        elif (self.aircraft_angle < -90) or (self.aircraft_angle > 90):
            print("Aircraft has exceeded safe bank angle. Simulation ending.")
            pyglet.app.exit()

        # Save position vs time data to txt file
        with open(self.data_path_name, "a") as f:
            stringified = str(self.x1) + " " + str(self.y1) + " " + str(self.bank1) + " " + str(self.runtime) + "\n"
            f.write(stringified)

        # Update camera
        self.cam_x, self.cam_y = self.camera()
        
        # Update HUD text
        self.label_pos.text = f"Aircraft init pos: ({self.aircraft_x:.1f}, {self.aircraft_y:.1f})"
        self.label_pitch.text = f"Bank: {self.aircraft_angle:.1f}°"


    def on_draw(self):
        self.clear()

        # Draw background
        self.background_img.blit(-self.cam_x, -self.cam_y)

        # Draw world grid
        gridx = pyglet.graphics.Batch()
        gridy = pyglet.graphics.Batch()
        for x in range(0, pic_width+1, 200):
            line = shapes.Line(x - self.cam_x, 0 - self.cam_y, x - self.cam_x, pic_height - self.cam_y, thickness=3, color=(150,150,205), batch=gridx)
            gridx.draw()
        for y in range(0, pic_height+1, 200):
            line = shapes.Line(0 - self.cam_x, y - self.cam_y, pic_width - self.cam_x, y - self.cam_y, thickness=3, color=(150,150,205), batch=gridy)
            gridy.draw()


        # --- ADD DRAW CODE - RYAN ---
        aircraft = pyglet.graphics.Batch() # create a batch of shapes for the aircraft

        length = 40
        wing = 100
        theta = math.radians(self.aircraft_angle)
        
        # define midpoint in relative coords
        # all coords are from bottom left, so this finds the relative coordinates in terms of the camera
        px = self.aircraft_x - self.cam_x
        py = self.aircraft_y - self.cam_y

        # set relative coords with respect to initial position
        self.relativex = self.aircraft_x - self.initx
        self.relativey = self.aircraft_y - self.inity

        #scaled relative coords
        srelativex = self.relativex * self.worldscale
        srelativey = self.relativey * self.worldscale
        
        self.plot_coordx = -self.cam_x + self.initx + srelativex
        self.plot_coordy = -self.cam_y + self.inity + srelativey


        #self.aircraft_sprite.anchor_x = wing/4
        #self.aircraft_sprite.anchor_y = length/4
        # must be negative to agree with convention. rolling right is positive bank angle for pilot's view, angle is between the (pilots) left wing and the horizontal
        self.aircraft_sprite.rotation = -self.aircraft_angle
        self.aircraft_sprite.x = self.plot_coordx
        self.aircraft_sprite.y = self.plot_coordy

        # draw aircraft
        #aircraft.draw()
        self.aircraft_sprite.draw()
        # Draw HUD
        self.label_pos.draw()
        self.label_pitch.draw()
        


if __name__ == "__main__":
    window = AircraftVisualizer()
    pyglet.app.run()



# todo:
'''
 figure out how to implement physics engine into visualizer
 we have numerical solution to system of odes
 time 

'''