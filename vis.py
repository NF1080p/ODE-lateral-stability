import pyglet
from pyglet import shapes
import math
from secondOrderDE import second_order_DE_nonlinear
from secondOrderDE import second_order_DE_nonlinear_rk4
from secondOrderDE import second_order_DE_nonlinear_rk4_one_step
from secondOrderDE import nick_test
import physics

# --- Constants ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
VIEWPORT_MARGIN = 100  # pixels from edge before camera moves

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

        # Aircraft init state
        # NOTE: COORDNIATES LOAD FROM BOTTOM LEFT
        # (0,0) is bottom-left of background image

        self.aircraft_x = pic_width/2
        self.aircraft_y = pic_height - WINDOW_HEIGHT/2
        self.aircraft_angle = 10.0  # degrees
        self.aircraft_dx = 0.0
        self.aircraft_dy = 0.0
        self.aircraft_dangle = 0.0

        # Camera init pos (defining top-left corner)
        self.cam_x = pic_width/2 - WINDOW_WIDTH / 2
        self.cam_y = pic_height

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
        


    def camera(self):
        # Camera
        left_edge = self.cam_x + VIEWPORT_MARGIN
        right_edge = self.cam_x + WINDOW_WIDTH - VIEWPORT_MARGIN
        bottom_edge = self.cam_y + VIEWPORT_MARGIN
        top_edge = self.cam_y + WINDOW_HEIGHT - VIEWPORT_MARGIN

        if self.aircraft_x < left_edge:
            self.cam_x = self.aircraft_x - VIEWPORT_MARGIN
        elif self.aircraft_x > right_edge:
            self.cam_x = self.aircraft_x - WINDOW_WIDTH + VIEWPORT_MARGIN

        if self.aircraft_y < bottom_edge:
            self.cam_y = self.aircraft_y - VIEWPORT_MARGIN
        elif self.aircraft_y > top_edge:
            self.cam_y = self.aircraft_y - WINDOW_HEIGHT + VIEWPORT_MARGIN

        # Clamp camera to world
        return (max(0, min(self.cam_x, pic_width - WINDOW_WIDTH)), max(0, min(self.cam_y, pic_height - WINDOW_HEIGHT)))

    def update(self, dt):
        self.runtime += dt
        
        # calculate new aircraft properties from previous
        self.x1, self.y1, self.bank1, self.dx1, self.dy1, self.dbank1 = nick_test(self.aircraft_x, self.aircraft_y, self.aircraft_angle, 
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
        

        # Update camera
        self.cam_x, self.cam_y = self.camera()
        
        # Update HUD text
        self.label_pos.text = f"Aircraft Pos: ({self.aircraft_x:.1f}, {self.aircraft_y:.1f})"
        self.label_pitch.text = f"Bank: {self.aircraft_angle:.1f}°"
        # should this be bank angle

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
        px = self.aircraft_x - self.cam_x
        py = self.aircraft_y - self.cam_y
        # create shape with center at px, py
        rectangle = shapes.Rectangle(px-wing/2, py-length/2, wing/2, length/2, color=(255, 22, 20), batch=aircraft)
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