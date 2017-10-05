import arcade
from models import World, Player

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TWO_PLAYER = False

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

        # Sync Position before update() at the first time
        self.set_position(self.model.x, self.model.y)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
 
    def draw(self):
        self.sync_with_model()
        super().draw()

class SoccerWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        # Store Backgound
        self.backgound = None
        arcade.set_background_color(arcade.color.GREEN)

        # Create Sprite
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player1_sprite = ModelSprite('images/player1.png',
                                           model=self.world.player1)
        self.ball_sprite = ModelSprite('images/ball.png', model=self.world.ball)
        
        ###
        if TWO_PLAYER:
            self.player2_sprite = ModelSprite('images/player1.png',
                                               model=self.world.player2)
        ###

    def setupStadium(self):
        # Set Backgound to field
        self.backgound = arcade.load_texture("images/field.png")

    def on_draw(self):
        arcade.start_render()
        # Draw backgound
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgound)
        
        ### GOAL AREA
        arcade.draw_lrtb_rectangle_filled(1205,1280,460,260,arcade.color.RED)
        arcade.draw_lrtb_rectangle_filled(0,75,460,260,arcade.color.RED)
        ###
        
        # Draw Sprite
        self.ball_sprite.draw()
        self.player1_sprite.draw()

        ###
        if TWO_PLAYER:
            self.player2_sprite.draw()
        ###

    def update(self, delta):
        # Update Object in World 
        self.world.update(delta)
        # When Player1 hit the ball
        if arcade.check_for_collision(self.ball_sprite, self.player1_sprite) :
            self.world.ball.speed = self.world.player1.kick_power
            self.world.ball.angle = self.world.player1.angle
        
        ###
        if TWO_PLAYER:
            if arcade.check_for_collision(self.ball_sprite, self.player2_sprite) :
                self.world.ball.speed = self.world.player2.kick_power
                self.world.ball.angle = self.world.player2.angle
        ###

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

def main():
    window = SoccerWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    # Setup to field
    window.setupStadium()
    arcade.run()
 
if __name__ == '__main__':
    main()