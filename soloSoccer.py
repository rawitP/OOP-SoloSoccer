import arcade
# Need pyglet for drawing text option.
import pyglet
from models import World, Player

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BORDER_SIZE = 50
GOAL_WIDTH = 100
GOAL_HEIGHT = 200
TWO_PLAYER = True

TEXTURES_PLAYER1 = ['images/player_blue/player0.png','images/player_blue/player1.png',
                    'images/player_blue/player2.png','images/player_blue/player0.png',
                    'images/player_blue/player4.png','images/player_blue/player5.png']
TEXTURES_PLAYER2 = ['images/player_red/player0.png','images/player_red/player1.png',
                    'images/player_red/player2.png','images/player_red/player0.png',
                    'images/player_red/player4.png','images/player_red/player5.png']


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


class AnimatedPositionSprite(arcade.Sprite):
    TEXTURE_CHANGE_DISTANCE = 15

    def __init__(self, textures_locations, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(textures_locations[0], **kwargs)

        # Sync Position before update() at the first time
        self.set_position(self.model.x, self.model.y)

        # Store previous position
        self.prev_x = self.center_x
        self.prev_y = self.center_y
        self.distance = 0

        # Store textures to textures_list
        self.textures_list = []
        for texture_location in textures_locations:
            self.textures_list.append(arcade.load_texture(texture_location))
        self.texture_change_distance = self.TEXTURE_CHANGE_DISTANCE

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def update_animation(self):
        # If not the same position, animate textures.
        # By using interval of distance.
        if self.center_x != self.prev_x or self.center_y != self.prev_y:
            # Store previous position before update texture
            self.prev_x = self.center_x
            self.prev_y = self.center_y
            self.distance  += self.model.speed
            texture_index = ((1 + int(self.distance//self.texture_change_distance)) %
                             len(self.textures_list))
            self.texture = self.textures_list[texture_index]
        else:
            self.texture = self.textures[0]
            self.distance = 0

    def draw(self):
        self.sync_with_model()
        self.update_animation()
        super().draw()


class WallSprite(arcade.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__('images/block.png')
        self.set_position(x, y)
        self.width = width
        self.height = height
        # Set the wall invisble
        self.alpha = 0 # 0 = invisible, 1 = visible

class TimerText():
    TIME_TEXT_SIZE = 28

    def __init__(self, **kwargs):
        self.timer = kwargs.pop('timer', None)
        self.time = ''
        self.time_text = arcade.create_text('', arcade.color.BLACK)

    def sync_time(self):
        self.time = '{:02d}:{:02d}'.format(self.timer.get_time() // 60, 
                                           self.timer.get_time() % 60)

    def draw(self):
        self.sync_time()
        if self.time != self.time_text.text:
            self.time_text = pyglet.text.Label(str(self.time),
                                font_name=('Calibri', 'Arial'),
                                font_size=self.TIME_TEXT_SIZE,
                                color=(arcade.color.BLACK + (127,)),
                                anchor_x="center",
                                anchor_y="center")
        arcade.render_text(self.time_text, SCREEN_WIDTH//2, SCREEN_HEIGHT - BORDER_SIZE//2)

class Text():
    TEXT_SIZE = 24
    TEXT_COLOR = arcade.color.BLACK
    ALPHA = 127

    def __init__(self, x, y, text_obj):
        self.text_obj = text_obj
        self.val = ''
        self.text = arcade.create_text('', arcade.color.BLACK)
        self.x = x
        self.y = y

    # Need to fix how to sync it
    def sync(self):
        self.val = self.text_obj
        print(self.text_obj)

    def draw(self):
        self.sync()
        if self.text.text != self.val:
            self.text = pyglet.text.Label(str(self.val),
                                font_name=('Calibri', 'Arial'),
                                font_size=self.SCORE_SIZE,
                                color=(TEXT_COLOR + (ALPHA,)),
                                anchor_x="center",
                                anchor_y="center")
        else:
            print('False')
        arcade.render_text(self.text, self.x, self.y)


class ResultText():
    SIZE = 48
    TEXT_COLOR = arcade.color.BLACK
    ALPHA = 255

    def __init__(self, x, y, **kwargs):
        self.world = kwargs.pop('world', None)
        self.val = ''
        self.text = arcade.create_text('', arcade.color.BLACK)
        self.x = x
        self.y = y

    def sync(self):
        self.val = self.world.team_winner

    def draw(self):
        self.sync()
        if self.text.text != self.val:
            if self.val != 'Draw' and self.val != '':
                self.val = '{0} is winner'.format(self.val)
            self.text = pyglet.text.Label(str(self.val),
                                font_name=('Calibri', 'Arial'),
                                font_size=ResultText.SIZE,
                                color=(ResultText.TEXT_COLOR + (ResultText.ALPHA,)),
                                anchor_x="center",
                                anchor_y="center")
        arcade.render_text(self.text, self.x, self.y)


class ScoreText():
    OFFSET_X = 20
    OFFSET_Y = 50
    SCORE_SIZE = 48

    def __init__(self, **kwargs):
        self.world = kwargs.pop('world', None)
        self.score_team_1 = 0
        self.score_team_2 = 0
        self.team_winner = ''
        self.text1 = arcade.create_text('', arcade.color.BLACK)
        self.text2 = arcade.create_text('', arcade.color.BLACK)
        #self.text_winner = arcade.create_text('', arcade.color.BLACK)
    
    def sync_score(self):
        self.score_team_1 = self.world.score.teams_score['Blue']
        self.score_team_2 = self.world.score.teams_score['Red']
        #self.team_winner = self.world.score.team_winner

    def draw(self):
        self.sync_score()
        if self.score_team_1 != self.text1.text:
            self.text1 = pyglet.text.Label(str(self.score_team_1),
                                font_name=('Calibri', 'Arial'),
                                font_size=self.SCORE_SIZE,
                                color=(arcade.color.BLUE + (127,)),
                                anchor_x="right",
                                anchor_y="top")
        if self.score_team_2 != self.text2.text:
            self.text2 = pyglet.text.Label(str(self.score_team_2),
                                font_name=('Calibri', 'Arial'),
                                font_size=self.SCORE_SIZE,
                                color=(arcade.color.RED + (127,)),
                                anchor_x="left",
                                anchor_y="top")
        '''
        if self.team_winner != self.text_winner.text:
            self.text_winner = pyglet.text.Label(str(self.team_winner + ' is winner'),
                                font_name=('Calibri', 'Arial'),
                                font_size=self.SCORE_SIZE,
                                color=(arcade.color.BLACK + (255,)),
                                anchor_x="center",
                                anchor_y="center")
        '''
        arcade.render_text(self.text1, SCREEN_WIDTH//2 - self.OFFSET_X,
                                       SCREEN_HEIGHT - self.OFFSET_Y)
        arcade.render_text(self.text2, SCREEN_WIDTH//2 + self.OFFSET_X,
                                       SCREEN_HEIGHT - self.OFFSET_Y)
        #arcade.render_text(self.text_winner, SCREEN_WIDTH//2 , SCREEN_HEIGHT // 2)


class SoccerWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        # Store Backgound
        self.backgound = None
        arcade.set_background_color(arcade.color.GREEN)

        # Create Sprite
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_sprite_list = arcade.SpriteList()
        self.player1_sprite = AnimatedPositionSprite(TEXTURES_PLAYER1,
                                                     model=self.world.player1)
        self.player_sprite_list.append(self.player1_sprite)
        self.ball_sprite = ModelSprite('images/ball.png', model=self.world.ball)
        
        # Create object for drawing text
        self.score_text = ScoreText(world=self.world)
        self.time_text = TimerText(timer=self.world.timer)
        self.result_text = ResultText(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, world=self.world)

        # Add Wall for bouncing
        self.wall_sprite_list = arcade.SpriteList()
        self.wall_top = WallSprite(SCREEN_WIDTH//2, SCREEN_HEIGHT - BORDER_SIZE//2, 
                                   SCREEN_WIDTH, BORDER_SIZE)
        self.wall_bottom = WallSprite(SCREEN_WIDTH//2, 0 + BORDER_SIZE//2, 
                                      SCREEN_WIDTH, BORDER_SIZE)
        self.wall_left_top = WallSprite(GOAL_WIDTH//2, SCREEN_HEIGHT//2 + GOAL_HEIGHT/2 + SCREEN_HEIGHT//2,
                                        GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_left_bottom = WallSprite(GOAL_WIDTH//2, SCREEN_HEIGHT//2 - GOAL_HEIGHT/2 - SCREEN_HEIGHT//2,
                                           GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_left_outside = WallSprite(-BORDER_SIZE//2, SCREEN_HEIGHT//2,
                                             BORDER_SIZE, SCREEN_HEIGHT)
        self.wall_right_top = WallSprite(SCREEN_WIDTH - GOAL_WIDTH//2, SCREEN_HEIGHT//2 + GOAL_HEIGHT/2 + SCREEN_HEIGHT//2,
                                         GOAL_WIDTH, SCREEN_HEIGHT)
        self.wall_right_bottom = WallSprite(SCREEN_WIDTH - GOAL_WIDTH//2, SCREEN_HEIGHT//2 - GOAL_HEIGHT/2 - SCREEN_HEIGHT//2,
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
        self.goal_1_sprite = arcade.Sprite('images/goal.png')
        self.goal_1_sprite.set_position(self.world.goal_1.center_x,
                                        self.world.goal_1.center_y)
        self.goal_2_sprite = arcade.Sprite('images/goal.png')
        self.goal_2_sprite.set_position(self.world.goal_2.center_x,
                                        self.world.goal_2.center_y)

        # Bot Player Sprite (Goalkeeper)
        self.bot_player_1_sprite = AnimatedPositionSprite(TEXTURES_PLAYER1,
                                                          model=self.world.bot_player_1)
        self.player_sprite_list.append(self.bot_player_1_sprite)
        self.bot_player_2_sprite = AnimatedPositionSprite(TEXTURES_PLAYER2,
                                                          model=self.world.bot_player_2)
        self.player_sprite_list.append(self.bot_player_2_sprite)

        ###
        if TWO_PLAYER:
            self.player2_sprite = AnimatedPositionSprite(TEXTURES_PLAYER2,
                                                         model=self.world.player2)
            self.player_sprite_list.append(self.player2_sprite)
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
        self.score_text.draw()
        self.time_text.draw()
        self.ball_sprite.draw()
        for player in self.player_sprite_list:
            player.draw()
        self.goal_1_sprite.draw()
        self.goal_2_sprite.draw()

        # Draw Winner
        self.result_text.draw()     

    def update(self, delta):
        # Update Object in World 
        self.world.update(delta)
        # Sync Ball model before check collision
        self.ball_sprite.sync_with_model()
        for player in self.player_sprite_list:
            player.sync_with_model()

        # When Player hit the ball
        for player in self.player_sprite_list:
            if arcade.check_for_collision(player, self.ball_sprite):
                player.model.prev_pos() # Player will not walk through the ball
                self.world.ball.go_speed_angle(player.model.kick_power, player.model.angle)

        # When Player hit the wall (Player have to stay inside border)
        for player in self.player_sprite_list:
            if (player.model.x > SCREEN_WIDTH - GOAL_WIDTH or
                    player.model.x < 0 + GOAL_WIDTH or
                    player.model.y > SCREEN_HEIGHT - BORDER_SIZE or
                    player.model.y < 0 + BORDER_SIZE):
                player.model.prev_pos()
        
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
