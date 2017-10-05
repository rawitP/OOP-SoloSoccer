import math
import arcade.key
import random

TWO_PlAYER = False

WIDTH = None
HEIGHT = None

class Ball:
    MOVE_ACC = -1
    BORDER_BOTTOM = 55
    BORDER_TOP = 665
    BORDER_LEFT = 75
    BORDER_RIGHT = 1205
    GOAL_SIZE = 200

    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = angle
        self.is_outside = False

    def update(self, delta):
        '''
        Bouncing at border
        UPDATE: Added goal area for boucing
        ''' 
        if not self.is_outside:
            # When ball outside line or goal
            if (self.x < self.BORDER_LEFT and
               (self.y > HEIGHT/2 + self.GOAL_SIZE / 2 or self.y < HEIGHT/2 - self.GOAL_SIZE / 2))\
                    or self.x < 0 :
                self.is_outside = True
                if self.angle % 360 > 180:
                    self.angle = 270 + (270 - self.angle)
                else:
                    self.angle = 90 - (self.angle - 90)
            elif (self.x > self.BORDER_RIGHT and 
                 (self.y > HEIGHT/2 + self.GOAL_SIZE / 2 or self.y < HEIGHT/2 - self.GOAL_SIZE / 2))\
                    or self.x > 1280 :
                self.is_outside = True
                if self.angle % 360 > 180:
                    print(self.angle % 360)
                    self.angle = 270 - (self.angle - 270)
                    print(self.angle % 360)
                else:
                    self.angle = 90 + (90 - self.angle)
            if self.y < self.BORDER_BOTTOM or\
                    (self.y < HEIGHT/2 - self.GOAL_SIZE / 2 and 
                    (self.x < self.BORDER_LEFT or self.x > self.BORDER_RIGHT)):
                print("y1")
                self.is_outside = True
                if self.angle % 360 > 270 :
                    self.angle = 90 - (self.angle - 270)
                else:
                    self.angle = 90 + (270 - self.angle)
            elif self.y > self.BORDER_TOP or\
                    (self.y > HEIGHT/2 + self.GOAL_SIZE / 2 and 
                    (self.x < self.BORDER_LEFT or self.x > self.BORDER_RIGHT)):
                print("y2")
                self.is_outside = True
                if self.angle % 360 > 90:
                    self.angle = 180 + (180 - self.angle)
                else:
                    self.angle = 360 - self.angle
        else:
            print("Outside naja")
            if self.x > self.BORDER_LEFT or self.x < self.BORDER_RIGHT or\
               self.y > self.BORDER_BOTTOM or self.y < self.BORDER_TOP:
                self.is_outside = False
        
        # Make it move realistic
        if self.speed > 0 :
            self.speed = self.speed + self.MOVE_ACC*(0.1) # v = u + at
            if self.speed < 0 :
                self.speed = 0
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed

class Player:
    TURN_SPEED = 3
    SPEED_DEFAULT = 3
    DEFAULT_KICK_POWER = 7

    def __init__(self, x, y, angle, speed=SPEED_DEFAULT):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.kick_power = self.DEFAULT_KICK_POWER
        self.is_walk = False
        self.turn_direction = [False, False] # [LEFT, RIGHT]

    def update(self, delta):
        if self.is_walk:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed
        # If it is turning
        if self.turn_direction[0]:
            self.angle += self.TURN_SPEED
        if self.turn_direction[1]:
            self.angle -= self.TURN_SPEED

class World:

    def __init__(self, width, height):
        global WIDTH; WIDTH = width
        global HEIGHT; HEIGHT = height
        self.width = width
        self.height = height
        self.player1 = Player(width // 2 * 0.5, height // 2, 0)
        self.ball = Ball(width // 2 , height // 2)

        ###
        if TWO_PlAYER:
            self.player2 = Player(width // 2 * 1.5, height // 2, 180)
        ###
 
    def update(self, delta):
        self.player1.update(delta)
        self.ball.update(delta)

        ###
        if TWO_PlAYER:
            self.player2.update(delta)
        ###

    def on_key_press(self, key, key_modifiers):
        # Player1 will walk
        if key == arcade.key.UP:
            self.player1.is_walk = True
        # Player1 will turn
        if key == arcade.key.RIGHT:
            self.player1.turn_direction[1] = True
        if key == arcade.key.LEFT:
            self.player1.turn_direction[0] = True

        ###
        if TWO_PlAYER:
            if key == arcade.key.W:
                self.player2.is_walk = True
            # Player1 will turn
            if key == arcade.key.D:
                self.player2.turn_direction[1] = True
            if key == arcade.key.A:
                self.player2.turn_direction[0] = True
        ###

    def on_key_release(self, key, key_modifiers):
        # Player1 will NOT walk
        if key == arcade.key.UP:
            self.player1.is_walk = False
        # Player1 will NOT turn
        if key == arcade.key.RIGHT:
            self.player1.turn_direction[1] = False
        if key == arcade.key.LEFT:
            self.player1.turn_direction[0] = False

        ###
        if TWO_PlAYER:
            if key == arcade.key.W:
                self.player2.is_walk = False
            # Player1 will NOT turn
            if key == arcade.key.D:
                self.player2.turn_direction[1] = False
            if key == arcade.key.A:
                self.player2.turn_direction[0] = False
        ###