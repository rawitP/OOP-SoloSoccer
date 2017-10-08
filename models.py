import math
import arcade.key
import random

TWO_PlAYER = True

WIDTH = None
HEIGHT = None

class Ball:
    MOVE_ACC = -1

    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.speed = 0
        self.angle = angle
        self.is_outside = False
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
    DEFAULT_KICK_POWER = 7
    COLLISION_RADIUS = 20

    def __init__(self, x, y, angle, speed=SPEED_DEFAULT):
        self.x = x
        self.y = y
        self.prev_x = None
        self.prev_y = None
        self.angle = angle
        self.speed = speed
        self.kick_power = self.DEFAULT_KICK_POWER
        self.is_walk = False
        self.turn_direction = [False, False] # [LEFT, RIGHT]

    def prev_pos(self):
        self.x = self.prev_x
        self.y = self.prev_y

    def update(self, delta):
        if self.is_walk:
            self.prev_x = self.x
            self.prev_y = self.y
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
        self.players = []
        self.player1 = Player(width // 2 * 0.5, height // 2, 0)
        self.players.append(self.player1)
        self.ball = Ball(width // 2 , height // 2)

        ###
        if TWO_PlAYER:
            self.player2 = Player(width // 2 * 1.5, height // 2, 180)
            self.players.append(self.player2)
        ###
 
    def update(self, delta):
        for player in self.players:
            player.update(delta)
        self.ball.update(delta)

        # Check for collision between players
        # By using distance between players
        for player in self.players:
            for other_player in self.players:
                if player is not other_player:
                    distance = math.sqrt(  ((player.x - other_player.x)**2)\
                                         + ((player.y - other_player.y)**2) )
                    if distance < (player.COLLISION_RADIUS +
                                  other_player.COLLISION_RADIUS):
                        player.prev_pos()

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
            # Player2 will NOT turn
            if key == arcade.key.D:
                self.player2.turn_direction[1] = False
            if key == arcade.key.A:
                self.player2.turn_direction[0] = False
        ###