import arcade
from models import World, Player

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BORDER_SIZE = 50
GOAL_WIDTH = 100
GOAL_HEIGHT = 200
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

class WallSprite(arcade.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__('images/block.png')
        self.set_position(x, y)
        self.width = width
        self.height = height
        self.alpha = 0

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
        
        # Add Wall for bouncing
        self.wall_sprite_list = arcade.SpriteList()
        self.wall_top = WallSprite(SCREEN_WIDTH//2, SCREEN_HEIGHT - BORDER_SIZE//2, 
                                   SCREEN_WIDTH, BORDER_SIZE)
        self.wall_bottom = WallSprite(SCREEN_WIDTH//2, 0 + BORDER_SIZE//2, 
                                      SCREEN_WIDTH, BORDER_SIZE)
        self.wall_left_top = WallSprite(GOAL_WIDTH//2, SCREEN_HEIGHT//2*2.25,
                                        GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_left_bottom = WallSprite(GOAL_WIDTH//2, SCREEN_HEIGHT//2*-0.25,
                                           GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_left_outside = WallSprite(-BORDER_SIZE//2, SCREEN_HEIGHT//2,
                                             BORDER_SIZE, SCREEN_HEIGHT)
        self.wall_right_top = WallSprite(SCREEN_WIDTH - GOAL_WIDTH//2, SCREEN_HEIGHT//2*2.25,
                                         GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_right_bottom = WallSprite(SCREEN_WIDTH - GOAL_WIDTH//2, SCREEN_HEIGHT//2*-0.25,
                                            GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_right_outside = WallSprite(SCREEN_WIDTH + BORDER_SIZE//2, SCREEN_HEIGHT//2,
                                             BORDER_SIZE, SCREEN_HEIGHT)
        self.wall_sprite_list.append(self.wall_top)
        self.wall_sprite_list.append(self.wall_bottom)
        self.wall_sprite_list.append(self.wall_left_top)
        self.wall_sprite_list.append(self.wall_left_bottom)
        self.wall_sprite_list.append(self.wall_left_outside)     
        self.wall_sprite_list.append(self.wall_right_top)
        self.wall_sprite_list.append(self.wall_right_bottom)
        self.wall_sprite_list.append(self.wall_right_outside)   

        # Add Goal Sprites for detect the ball
        self.goal_area_1 = arcade.Sprite('images/goal.png')
        self.goal_area_1.set_position(50, SCREEN_HEIGHT//2)
        self.goal_area_2 = arcade.Sprite('images/goal.png')
        self.goal_area_2.set_position(SCREEN_WIDTH - (GOAL_WIDTH//2), SCREEN_HEIGHT//2)

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

        # Draw Sprite
        self.wall_sprite_list.draw()
        self.ball_sprite.draw()
        self.player1_sprite.draw()
        self.goal_area_1.draw()
        self.goal_area_2.draw()

        ###
        if TWO_PLAYER:
            self.player2_sprite.draw()
        ###

    def update(self, delta):
        # Update Object in World 
        self.world.update(delta)
        self.ball_sprite.sync_with_model()
        # When Player1 hit the ball
        if arcade.check_for_collision(self.ball_sprite, self.player1_sprite) :
            self.world.ball.speed = self.world.player1.kick_power
            self.world.ball.angle = self.world.player1.angle
        
        '''
        Check For collision between ball and walls.

        Concept:
        + + + + + + +
        +       # # # # #  |
        +       #   +   #  | dist_y
        + + + + # + +   #  |
                # # # # #
                _ _ _ 
                dist_x

        '''
        hit_walls = arcade.check_for_collision_with_list(self.ball_sprite, 
                                                         self.wall_sprite_list)
        for wall in hit_walls:
            # Right side
            if self.ball_sprite.right > wall.right:
                dist_x = wall.right - self.ball_sprite.left
                if self.ball_sprite.bottom < wall.bottom:
                    dist_y = self.ball_sprite.top - wall.bottom
                    if dist_x > dist_y:
                        #print("Go Bottom_Left")
                        self.world.ball.bounce_to_bottom()
                        self.world.ball.prev_pos()
                    elif dist_x == dist_y:
                        #print("Go Reverse")
                        self.world.ball.bounce_reverse()
                        self.world.ball.prev_pos()
                    else:
                        #print("Go Right_Top")
                        self.world.ball.bounce_to_right()
                        self.world.ball.bounce_to_right
                    self.world.ball.prev_pos()
                elif self.ball_sprite.top > wall.top:
                    dist_y = wall.top - self.ball_sprite.bottom
                    if dist_x > dist_y:
                        #print("Go Top_Left")
                        self.world.ball.bounce_to_top()
                        self.world.ball.prev_pos()
                    elif dist_x == dist_y:
                        #print("Go Reverse")
                        self.world.ball.bounce_reverse()
                        self.world.ball.prev_pos()
                    else:
                        #print("Go Right_Bottom")
                        #print(dist_x, dist_y)
                        self.world.ball.bounce_to_right()
                        self.world.ball.prev_pos()
                else:
                    #print("Go Right_?")
                    self.world.ball.bounce_to_right()
                    self.world.ball.prev_pos()
            # Left side
            elif self.ball_sprite.left < wall.left:
                dist_x = self.ball_sprite.right - wall.left
                if self.ball_sprite.bottom < wall.bottom:
                    dist_y = self.ball_sprite.top - wall.bottom
                    if dist_x > dist_y:
                        #print("Go Bottom_Right")
                        self.world.ball.bounce_to_bottom()
                        self.world.ball.prev_pos()
                    elif dist_x == dist_y:
                        #print("Go Reverse")
                        self.world.ball.bounce_reverse()
                        self.world.ball.prev_pos()
                    else:
                        #print("Go LEFT_Top")
                        self.world.ball.bounce_to_left()
                        self.world.ball.prev_pos()
                elif self.ball_sprite.top > wall.top:
                    dist_y = wall.top - self.ball_sprite.bottom
                    if dist_x > dist_y:
                        #print("Go Top_Right")
                        #print(dist_x, dist_y)
                        self.world.ball.bounce_to_top()
                        self.world.ball.prev_pos()
                    elif dist_x == dist_y:
                        #print("Go Reverse")
                        self.world.ball.bounce_reverse()
                        self.world.ball.prev_pos()
                    else:
                        #print("Go Left_Bottom")
                        self.world.ball.bounce_to_left()
                        self.world.ball.prev_pos()
                else:
                    #print("Go Left_?")
                    self.world.ball.bounce_to_left()
                    self.world.ball.prev_pos()
            else:
                #print("Go Top/Bottom")
                if self.ball_sprite.center_y < wall.change_y:
                    self.world.ball.bounce_to_bottom()
                else:
                    self.world.ball.bounce_to_top()
                self.world.ball.prev_pos()

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
