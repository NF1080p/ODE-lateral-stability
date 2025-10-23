import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = arcade.color.SKY_BLUE


class AircraftVisualizer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Aircraft Visualization")
        arcade.set_background_color(BACKGROUND_COLOR)
        self.aircraft_x = 200
        self.aircraft_y = 300
        self.aircraft_angle = 0.0  # radians or degrees

    def on_update(self, delta_time):
        # TODO: Replace with physics engine updates
        self.aircraft_x += 50 * delta_time   # placeholder forward motion
        self.aircraft_angle += 10 * delta_time  # placeholder rotation

    def on_draw(self):
        # NEW: use clear() instead of start_render()
        self.clear()

        # Draw simple aircraft (triangle)
        length = 40
        wing = 15
        points = [
            (self.aircraft_x + length, self.aircraft_y),
            (self.aircraft_x - length, self.aircraft_y - wing),
            (self.aircraft_x - length, self.aircraft_y + wing),
        ]
        arcade.draw_polygon_filled(points, arcade.color.DARK_GRAY)

        # HUD text
        arcade.draw_text(f"Pitch: {self.aircraft_angle:.2f}",
                         20, 20, arcade.color.BLACK, 14)


if __name__ == "__main__":
    window = AircraftVisualizer()
    arcade.run()
