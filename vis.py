import pyglet
from pyglet import shapes
import math
from secondOrderDE import second_order_DE_nonlinear_rk4_one_step
from pathlib import Path
from datetime import datetime
import numpy as np
import physics
import keyboardctrl


# --- Constants ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700  # pixels from edge before camera moves

NUM_OF_FRAMES = 60
SIM_TIME = 20 
# Background image
# https://unsplash.com/photos/sky-cloud-blue-background-paronama-web-cloudy-summer-winter-season-day-light-beauty-horizon-spring-brigth-gradient-calm-abstract-backdrop-air-nature-view-wallpaper-landscape-cyan-color-environment-wkVWKgeyEEs
# 3000x1097
pic_width = 3000
pic_height = 1097

# --- Aircraft Visualizer ---
class AircraftVisualizer(pyglet.window.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Aircraft Visualizer - Pyglet 2.x")
        pyglet.gl.glClearColor(0.53, 0.81, 0.98, 1.0)  # Sky blue background

        

        # Initialize physics variables
        physics.globalize_physics_vars(dihedral=5, Mass=1000, WingLength=4, WingWidth=1, BodyArea=5,
                                       cLift_a0=0.25, cL_slope=0.2,
                                       altitude=1000, cruise=52, I_roll=1000, drag_mult = 1)
        
        self.aircraft_angle = 20.0  # degrees
        self.worldscale = 10  # zoom level
        
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

        # Camera init pos (defining top-left corner)
        self.cam_x = pic_width/2 - WINDOW_WIDTH / 2
        self.cam_y = pic_height
        print(f"Initial camera position: ({self.cam_x}, {self.cam_y})")
        
        # store flight data

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # remove problematic characters
        self.data_path_name = Path("data") / f"data-{timestamp}.txt"

        # HUD labels
        self.label_pos = pyglet.text.Label('', x=10, y=WINDOW_HEIGHT-30)
        self.label_pitch = pyglet.text.Label('', x=10, y=WINDOW_HEIGHT-60)
        self.autopilot_status = pyglet.text.Label('', x=10, y=WINDOW_HEIGHT-90)


        
        # 60 FPS
        pyglet.clock.schedule_interval(self.update, float(1/NUM_OF_FRAMES))

        # Load background image
        self.background_img = pyglet.image.load("background.jpeg")
        self.background_img.anchor_x = 0
        self.background_img.anchor_y = 0
        self.runtime = 0.0
        
        # Camera variables
        self.VIEWPORT_MARGIN = 200  # pixels from edge before camera moves

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


        #print(f"Aircraft position: ({self.scaled_aircraft_x}, {self.scaled_aircraft_y})")

        if (self.scaled_aircraft_x) < left_edge:
            self.cam_x = self.scaled_aircraft_x - self.VIEWPORT_MARGIN
        elif self.scaled_aircraft_x > right_edge:
            self.cam_x = self.scaled_aircraft_x - WINDOW_WIDTH + self.VIEWPORT_MARGIN

        if self.scaled_aircraft_y < bottom_edge:
            self.cam_y = self.scaled_aircraft_y - self.VIEWPORT_MARGIN
        elif self.scaled_aircraft_y > top_edge:
            self.cam_y = self.scaled_aircraft_y - WINDOW_HEIGHT + self.VIEWPORT_MARGIN
        #print(f"Updated camera position: ({self.cam_x}, {self.cam_y})")

        # Clamp camera to world
        return (max(0, min(self.cam_x, pic_width - WINDOW_WIDTH)), max(0, min(self.cam_y, pic_height - WINDOW_HEIGHT)))

    def update(self, dt):
        self.runtime += dt
        
        # calculate new aircraft properties from previous
        self.x1, self.y1, self.bank1, self.dx1, self.dy1, self.dbank1 = second_order_DE_nonlinear_rk4_one_step(self.aircraft_x, self.aircraft_y, self.aircraft_angle, 
                                                                                                               self.aircraft_dx, self.aircraft_dy, self.aircraft_dangle, 
                                                                                                               1/NUM_OF_FRAMES)

        #print(f"Time: {self.runtime:.2f}s, Pos: ({self.x1:.2f}, {self.y1:.2f}), Angle: {self.bank1:.2f}°, Vel: ({self.dx1:.2f}, {self.dy1:.2f}), Angular Vel: {self.dbank1:.2f}°/s")
       
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

        # save position vs time data to txt file
        with open(self.data_path_name, "a") as f:
            stringified = str(self.x1) + " " + str(self.y1) + " " + str(self.bank1) + " " + str(self.runtime) + "\n"
            f.write(stringified)

        # Update camera
        self.cam_x, self.cam_y = self.camera()
        
        # Update HUD text
        self.label_pos.text = f"Aircraft init pos: ({self.aircraft_x:.1f}, {self.aircraft_y:.1f})"
        self.label_pitch.text = f"Bank: {self.aircraft_angle:.1f}°"
        #self.autopilot_status.text = f"Autopilot status: {keyboardctrl.ap_on:.1f}°"


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

        # create shape with center at px, py
        rectangle = shapes.Rectangle(self.plot_coordx-wing/2, self.plot_coordy-length/2, wing/2, length/2, color=(255, 22, 20), batch=aircraft)
        # rotation
        rectangle.anchor_x = wing/4
        rectangle.anchor_y = length/4
        # must be negative to agree with convention. rolling right is positive bank angle for pilot's view, angle is between the (pilots) left wing and the horizontal
        rectangle.rotation = -self.aircraft_angle

        # draw aircraft
        aircraft.draw()

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