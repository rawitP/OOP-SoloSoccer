import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class SoccerWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        # Store Backgound
        self.backgound = None
        arcade.set_background_color(arcade.color.GREEN)

    def setupStadium(self):
        # Set Backgound to field
        self.backgound = arcade.load_texture("images/field.png")

    def on_draw(self):
        arcade.start_render()

        # Draw backgound
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgound)

def main():
    window = SoccerWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    window.setupStadium()
    arcade.run()
 
if __name__ == '__main__':
    main()