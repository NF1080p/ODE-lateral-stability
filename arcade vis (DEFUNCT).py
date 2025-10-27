import arcade
import math

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
VIEWPORT_MARGIN = 100  # px from edge before camera recenters
BACKGROUND_COLOR = arcade.color.SKY_BLUE
CAMERA_SMOOTHING = 8.0  # larger -> snappier camera, smaller -> slower smoothing

class AircraftVisualizer(arcade.Window):
    def __init__(self):
        # init background
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Aircraft Visualization - Camera2D fixed")
        # https://unsplash.com/photos/sky-cloud-blue-background-paronama-web-cloudy-summer-winter-season-day-light-beauty-horizon-spring-brigth-gradient-calm-abstract-backdrop-air-nature-view-wallpaper-landscape-cyan-color-environment-wkVWKgeyEEs
        # 3000x1097
        self.pic_width = 3000
        self.pic_height = 1097

        self.background = arcade.load_texture("assets/background.jpeg")
        arcade.set_background_color(BACKGROUND_COLOR)

        self.background = arcade.load_texture("assets/background.jpeg")

        # initial state (replace with your physics outputs)
        self.aircraft_x = 200.0
        self.aircraft_y = 300.0
        self.aircraft_angle = 0.0  # degrees

        # max world dimensions
        self.world_width = self.pic_width
        self.world_height = self.pic_height

        # Camera, init at center of screen
        self.camera = arcade.camera.Camera2D()

        half_w = SCREEN_WIDTH / 2.0
        half_h = SCREEN_HEIGHT / 2.0
        self.camera.position = (half_w, half_h)


    def camera_slide(self, delta_time: float = 1/60.0):
        # Get current camera center
        cam_pos = self.camera.position  # pyglet.math.Vec2
        cam_x, cam_y = float(cam_pos.x), float(cam_pos.y)

        half_w = SCREEN_WIDTH / 2.0
        half_h = SCREEN_HEIGHT / 2.0

        # World-space edges of the visible area
        left_edge = cam_x - half_w
        right_edge = cam_x + half_w
        bottom_edge = cam_y - half_h
        top_edge = cam_y + half_h

        # Compute target camera center (start as current)
        target_x = cam_x
        target_y = cam_y
        changed = False

        # If aircraft is within margin of left/right edge, shift target
        if self.aircraft_x < left_edge + VIEWPORT_MARGIN:
            # put aircraft VIEWPORT_MARGIN from left edge
            target_x = self.aircraft_x - ( -half_w + VIEWPORT_MARGIN )
            changed = True
        elif self.aircraft_x > right_edge - VIEWPORT_MARGIN:
            target_x = self.aircraft_x - ( half_w - VIEWPORT_MARGIN )
            changed = True

        # Vertical
        if self.aircraft_y < bottom_edge + VIEWPORT_MARGIN:
            target_y = self.aircraft_y - ( -half_h + VIEWPORT_MARGIN )
            changed = True
        elif self.aircraft_y > top_edge - VIEWPORT_MARGIN:
            target_y = self.aircraft_y - ( half_h - VIEWPORT_MARGIN )
            changed = True

        if changed:
            # Clamp the target so the camera doesn't show outside world bounds
            target_x = max(half_w, min(target_x, self.world_width - half_w))
            target_y = max(half_h, min(target_y, self.world_height - half_h))
        else:
            # no target change: keep current camera center
            target_x, target_y = cam_x, cam_y

        # Smoothly interpolate camera position toward the target
        # simple exponential / critically-damped style lerp:
        t = 1.0 - math.exp(-CAMERA_SMOOTHING * self.delta_time)

        return cam_x + (target_x - cam_x) * t , cam_y + (target_y - cam_y) * t


    def on_update(self, delta_time: float):
        # -------------------------
        # Replace this placeholder with your physics engine step
        # Example simple motion so you can see camera behavior:
        self.aircraft_x += 200.0 * delta_time   # forward motion
        self.aircraft_y += 40.0 * delta_time    # slight climb
        self.aircraft_angle += 5.0 * delta_time
        # -------------------------

        # Assign new camera position (position setter provided by Camera2D)
        new_cam_x, new_cam_y = self.camera_slide(delta_time)
        self.camera.position = (new_cam_x, new_cam_y)

    def on_draw(self):
        self.clear()
        # Activate camera (transform world-to-screen)
        with self.camera.activate():
            # Draw world background
            arcade.draw_texture_rect(0, self.world_width, 0, self.world_height, self.background) 
            arcade.draw_line(0, 100, self.world_width, 100, arcade.color.DARK_GREEN, 3)

            # Draw grid (world coords)
            grid_spacing = 200
            for x in range(0, self.world_width + 1, grid_spacing):
                arcade.draw_line(x, 0, x, self.world_height, arcade.color.LIGHT_GRAY, 1)
            for y in range(0, self.world_height + 1, grid_spacing):
                arcade.draw_line(0, y, self.world_width, y, arcade.color.LIGHT_GRAY, 1)

            # Draw aircraft as rotated triangle (world coords)
            length = 40
            wing = 15
            theta = math.radians(self.aircraft_angle)
            local_pts = [(length, 0), (-length, -wing), (-length, wing)]
            world_pts = []
            for px, py in local_pts:
                rx = px * math.cos(theta) - py * math.sin(theta)
                ry = px * math.sin(theta) + py * math.cos(theta)
                world_pts.append((self.aircraft_x + rx, self.aircraft_y + ry))
            arcade.draw_polygon_filled(world_pts, arcade.color.DARK_GRAY)

        # HUD (drawn in screen coordinates, not affected by camera)
        arcade.draw_text(f"Aircraft Pos: ({self.aircraft_x:.1f}, {self.aircraft_y:.1f})",
                         10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 14)
        arcade.draw_text(f"Pitch: {self.aircraft_angle:.1f}°",
                         10, SCREEN_HEIGHT - 50, arcade.color.BLACK, 14)


if __name__ == "__main__":
    window = AircraftVisualizer()
    arcade.run()
