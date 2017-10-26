# TODO: New control movement
# Fix Goalkeeper and control movement

import math
import arcade.key
import random

TWO_PlAYER = True

WIDTH = 1280
HEIGHT = 720
GOAL_WIDTH = 100
GOAL_HEIGHT = 200

MAX_SCORE = 3
MAX_TIME = 60

class Goal:
    def __init__(self, x, y, width, height, team_target):
        self.team_target = team_target # Use to indicate which team will get score
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        ''' Uncomment for using Auto Enable/Disable
        # Use for enable/disable counting (detecting ball)
        self.is_counting = True
        '''

    def is_ball_inside(self, ball):
        # Every parts of ball have to stay inside goal
        is_inside = ball.x + ball.radius <= self.center_x + self.width/2 and\
                        ball.x - ball.radius >= self.center_x - self.width/2 and\
                        ball.y + ball.radius <= self.center_y + self.height/2 and\
                        ball.y - ball.radius >= self.center_y - self.height/2
        if is_inside:
            ''' Uncomment for Auto Disable            
            if self.is_counting:
                # Disable counting when the ball is inside.
                self.is_counting = False
            '''
            return True
        else:
            ''' UnComment for Auto Enable
            # Enable counting when ANY parts of ball is outside.
            self.is_counting = True
            '''
        return False

class Ball:
    MOVE_ACC = -1
    DEFAULT_RADIUS = 45/2

    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.radius = self.DEFAULT_RADIUS
        self.speed = 0
        self.angle = angle
        self.prev_x = self.x
        self.prev_y = self.y

    def prev_pos(self):
        self.x = self.prev_x
        self.y = self.prev_y

    def go_speed_angle(self, speed, angle):
        self.speed = speed
        self.angle = angle

    def bounce_reverse(self):
        self.angle = self.angle + 180

    def bounce_to_top(self):
        # Go Right
        if self.angle > 270:
            self.angle = 90 - (self.angle - 270)
        # Go Left
        else:
            self.angle = 90 + (270 - self.angle)

    def bounce_to_bottom(self):
        # Go Left
        if self.angle > 90:
            self.angle = 270 - (self.angle - 90)
        # Go Right
        else:
            self.angle = 270 + (90 - self.angle)

    def bounce_to_left(self):
        # Go Down
        if self.angle > 180:
            self.angle = 180 + (360 - self.angle)
        # Go UP
        else:
            self.angle = 180 - (self.angle - 0)

    def bounce_to_right(self):
        # Go Down
        if self.angle > 180:
            self.angle = 270 + (270 - self.angle)
        # Go UP
        else:
            self.angle = 0 + (180 - self.angle)
   
    def get_side(self):
        if self.x > WIDTH//2:
            return 1
        return 0

    def update(self, delta):
        # Make it move realistic
        if self.speed > 0 :
            self.prev_x = self.x
            self.prev_y = self.y
            self.speed = self.speed + self.MOVE_ACC*(0.1) # v = u + at
            if self.speed < 0 :
                self.speed = 0
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed 

class Player:
    TURN_SPEED = 3
    SPEED_DEFAULT = 3
    DEFAULT_KICK_POWER = 10
    COLLISION_RADIUS = 15
    DEFAULT_KICK_RUN = 4

    def __init__(self, x, y, angle, speed=SPEED_DEFAULT):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.angle = angle
        self.speed = speed
        self.kick_power = self.DEFAULT_KICK_RUN
        self.is_walk = False
        self.turn_direction = [False, False] # [LEFT, RIGHT]
        self.kick = False

    def prev_pos(self):
        self.x = self.prev_x
        self.y = self.prev_y

    def set_kick(self, is_kick):
        if is_kick:
            self.kick = True
            self.kick_power = self.DEFAULT_KICK_POWER
        else:
            self.kick = False
            self.kick_power = self.DEFAULT_KICK_RUN

    def update(self, delta):
        if self.is_walk:
            # Store previous position
            self.prev_x = self.x
            self.prev_y = self.y
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed
        # If it is turning
        if self.turn_direction[0]:
            self.angle += self.TURN_SPEED
        if self.turn_direction[1]:
            self.angle -= self.TURN_SPEED

class BotPlayer(Player):
    SPEED_DEFAULT = 0.75
    SIDE_RANGE = GOAL_HEIGHT//2
    DEFAULT_KICK_RUN = 7

    def __init__(self, x, y, angle, speed=SPEED_DEFAULT):
        super().__init__(x, y, angle, speed)
        self.default_angle = angle
        self.side = self.get_side() # 0=left 1=right

    def get_side(self):
        if self.x > WIDTH//2:
            return 1
        return 0

    def follow_ball(self, ball):
        if ball.y - self.y > 1 and self.y < HEIGHT//2 + self.SIDE_RANGE and\
           ball.get_side() == self.side:
            self.is_walk = True
            self.angle = 90
        elif ball.y - self.y < -1 and self.y > HEIGHT//2 - self.SIDE_RANGE and\
            ball.get_side() == self.side:
            self.is_walk = True
            self.angle = 270
        else:
            self.angle = self.default_angle
            self.is_walk = False

    def update(self, delta, ball):
        self.follow_ball(ball)
        if self.is_walk:
            # Store previous position
            # self.prev_x = self.x
            self.prev_y = self.y
            # self.x += math.cos(math.radians(self.angle)) * self.speed
            if abs(self.y - ball.y) > 1:
                self.y += math.sin(math.radians(self.angle)) * self.speed

class Score:
    def __init__(self):
        self.teams_score = {}

    def add_team(self, team_name):
        self.teams_score[team_name] = 0

    def check_winner(self, check_score):
        for team in self.teams_score.keys():
            if self.teams_score[team] == check_score:
                return team
        return ''

    def check_most(self):
        max = -1
        team = ''
        for cur_team in self.teams_score.keys():
            if self.teams_score[cur_team] > max:
                max = self.teams_score[cur_team]
                team = cur_team
            elif self.teams_score[cur_team] == max:
                team = 'Draw'
        return team


    def increase_score(self, team_name):
        self.teams_score[team_name] += 1

    def reset_score(self):
        for team in self.teams_score.keys():
            self.teams_score[team] = 0


class Timer():
    ON = 1
    OFF = 0
    COUNTDOWN_TYPE = 1
    CLOCK_TYPE = 0

    def __init__(self):
        self.time = 0
        self.status = Timer.OFF
        self.timer_type = Timer.CLOCK_TYPE

    def set_to_countdown(self, start_second):
        self.timer_type = Timer.COUNTDOWN_TYPE
        self.time = start_second

    def set_status(self, status):
        self.status = status

    def set_time(self, time):
        self.time = time

    def get_time(self):
        return int(round(self.time))

    def reset(self):
        self.timer_type = Timer.CLOCK_TYPE
        self.set_time(0)

    def update(self, delta):
        if self.status == self.ON: 
            if self.timer_type == Timer.CLOCK_TYPE:
                self.time += delta
            elif self.timer_type == Timer.COUNTDOWN_TYPE:
                self.time -= delta


class World:
    PLAYER_INIT_POS = ((WIDTH // 2 * 0.75, HEIGHT // 2, 0),
                       (WIDTH // 2 * 1.25, HEIGHT // 2, 180))
    BOT_INIT_POS = ((WIDTH // 2 * 0.22, HEIGHT // 2, 0),
                       (WIDTH // 2 * 1.78, HEIGHT // 2, 180))
    PLAYING_STATUS = 1
    NOT_PLAYING_STATUS = 0
    TITLE_STATUS = 2

    def __init__(self, width, height):
        global WIDTH
        WIDTH = width
        global HEIGHT
        HEIGHT = height
        self.width = width
        self.height = height
        self.game_status = World.TITLE_STATUS # 0 = NOT playing, 1 = playing

        # Player models
        self.all_players = []
        self.players = []
        self.player1 = Player(self.PLAYER_INIT_POS[0][0], self.PLAYER_INIT_POS[0][1],
                              self.PLAYER_INIT_POS[0][2])
        self.players.append(self.player1)
        self.all_players.append(self.player1)
        self.ball = Ball(width // 2 , height // 2)
        ###
        if TWO_PlAYER:
            self.player2 = Player(self.PLAYER_INIT_POS[1][0], self.PLAYER_INIT_POS[1][1],
                                  self.PLAYER_INIT_POS[1][2])
            self.all_players.append(self.player2)
            self.players.append(self.player2)
        ###
 
        # New Score Class
        self.score = Score()
        self.team_winner = ''

        # Create Timer
        self.timer = Timer()
        self.timer.set_status(Timer.ON)
        self.timer.set_to_countdown(MAX_TIME)

        '''
        Goal Section
        '''
        self.goals = []
        # Blue team Goal
        self.goal_1 = Goal(GOAL_WIDTH//2, HEIGHT//2,
                           GOAL_WIDTH, GOAL_HEIGHT, 'Red')
        self.goals.append(self.goal_1)
        # Red team Goal
        self.goal_2 = Goal(WIDTH - (GOAL_WIDTH//2), HEIGHT//2, 
                           GOAL_WIDTH, GOAL_HEIGHT, 'Blue')
        self.goals.append(self.goal_2)
        for goal in self.goals:
            self.score.add_team(goal.team_target)

        # Bot Player (Goalkeeper)
        self.bot_players = []
        self.bot_player_1 = BotPlayer(self.BOT_INIT_POS[0][0], self.BOT_INIT_POS[0][1],
                                      self.BOT_INIT_POS[0][2])
        self.all_players.append(self.bot_player_1)
        self.bot_players.append(self.bot_player_1)
        self.bot_player_2 = BotPlayer(self.BOT_INIT_POS[1][0], self.BOT_INIT_POS[1][1],
                                      self.BOT_INIT_POS[1][2])
        self.all_players.append(self.bot_player_2)
        self.bot_players.append(self.bot_player_2)

    def set_all_init_pos(self):
        # Set player positioin
        for player, init_pos in zip(self.players, self.PLAYER_INIT_POS):
            player.x = init_pos[0]
            player.y = init_pos[1]
            player.angle = init_pos[2]
            player.prev_x = player.x
            player.prev_y = player.y
        # Set Bot position
        for bot, init_pos in zip(self.bot_players, self.BOT_INIT_POS):
            bot.x = init_pos[0]
            bot.y = init_pos[1]
            bot.angle = init_pos[2]
            bot.prev_x = bot.x
            bot.prev_y = bot.y
        # Set ball position
        self.ball.x = WIDTH // 2
        self.ball.y = HEIGHT // 2
        self.ball.speed = 0
        self.ball.angle = 0

    def update(self, delta):
        # Models will not update when game_status = 0,1
        if self.game_status not in [World.PLAYING_STATUS,World.NOT_PLAYING_STATUS]:
            return

        for player in self.players:
            player.update(delta)
        self.ball.update(delta)

        for bot_player in self.bot_players:
            bot_player.update(delta, self.ball)

        # Check for collision between players
        # By using distance between players (Circle)
        for player in self.all_players:
            for other_player in self.all_players:
                if player is not other_player:
                    distance = math.sqrt(  ((player.x - other_player.x)**2)\
                                         + ((player.y - other_player.y)**2) )
                    if distance < (player.COLLISION_RADIUS +
                                  other_player.COLLISION_RADIUS):
                        player.prev_pos()

        # If game still running
        if self.game_status == 1:
            # Update timer
            self.timer.update(delta)
            # Check if ball is inside goal.
            for goal in self.goals:
                if goal.is_ball_inside(self.ball):
                    self.score.increase_score(goal.team_target)
                    self.team_winner = self.score.check_winner(MAX_SCORE)
                    self.game_status = 0
                    break
            # If timeout
            if self.timer.get_time() == 0:
                self.timer.set_time(0)
                self.team_winner = self.score.check_most()
                self.game_status = 0

    def on_key_press(self, key, key_modifiers):
        # Press Enter to Play Game
        if self.game_status not in [World.PLAYING_STATUS,World.NOT_PLAYING_STATUS]:
            if key == arcade.key.ENTER:
                self.game_status = 0
            return

        # Game control
        if key == arcade.key.R and self.game_status == 0:
            if self.team_winner != '':
                self.team_winner = ''
                self.timer.set_to_countdown(MAX_TIME)
                self.score.reset_score()
            self.game_status = 1
            self.set_all_init_pos()

        # Player1 will walk
        if key == arcade.key.W:
            self.player1.is_walk = True
        # Player1 will turn
        if key == arcade.key.D:
            self.player1.turn_direction[1] = True
        if key == arcade.key.A:
            self.player1.turn_direction[0] = True
        # Press ENter to kick the ball
        if key == arcade.key.SPACE:
            self.player1.set_kick(True)

        ###
        if TWO_PlAYER:
            if key == arcade.key.UP:
                self.player2.is_walk = True
            # Player2 will turn
            if key == arcade.key.RIGHT:
                self.player2.turn_direction[1] = True
            if key == arcade.key.LEFT:
                self.player2.turn_direction[0] = True
            # Press ENter to kick the ball
            if key == arcade.key.RCTRL:
                self.player2.set_kick(True)
        ###

    def on_key_release(self, key, key_modifiers):
        # Player1 will NOT walk
        if key == arcade.key.W:
            self.player1.is_walk = False
        # Player1 will NOT turn
        if key == arcade.key.D:
            self.player1.turn_direction[1] = False
        if key == arcade.key.A:
            self.player1.turn_direction[0] = False
        # Release Enter to NOT Kick the ball
        if key == arcade.key.SPACE:
            self.player1.set_kick(False)

        ###
        if TWO_PlAYER:
            if key == arcade.key.UP:
                self.player2.is_walk = False
            # Player2 will NOT turn
            if key == arcade.key.RIGHT:
                self.player2.turn_direction[1] = False
            if key == arcade.key.LEFT:
                self.player2.turn_direction[0] = False
            # Release Enter to NOT Kick the ball
            if key == arcade.key.RCTRL:
                self.player2.set_kick(False)
        ###