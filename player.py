'''
This module implements the player class which will keep track
of player location and allow for movement around environment
'''

import math

class Player(object):
    def __init__(self, x: float, y: float, angle: int) -> None:
        '''
        @attribute move_speed: Translation speed
        @attribute turn_speed: Rotation speed
        @attribute visual_field_degrees: Degrees that a player can see their environent. Half to left and half to right.
        '''
        self.x = x
        self.y = y
        self.angle = angle
        self.move_speed = 2
        self.turn_speed = 5
        self.visual_field_degrees = 90

    def _move(self, dir):
        '''
        @param dir: String 'UP' or 'DOWN'

        Update x and y position in the direction player is facing
        '''
        angle_radians = math.radians(self.angle)
        x_component = math.cos(angle_radians) * self.move_speed
        y_component = math.sin(angle_radians) * self.move_speed

        if dir == 'UP':
            self.x += x_component
            self.y += y_component
        else:
            self.x -= x_component
            self.y -= y_component

    def _rotate(self, dir):
        '''
        @param dir: String 'LEFT' or 'RIGHT'

        Change the players angle
        '''
        if dir == 'LEFT':
            self.angle -= self.turn_speed
        else:
            self.angle += self.turn_speed

    def key_input(self, key):
        '''
        @param key: String (UP, DOWN, LEFT, RIGHT)

        Interface that recieves keyboard input and routes it to appropriate methods
        '''
        if key == 'UP' or key == 'DOWN':
            self._move(key)
        elif key == 'LEFT' or key == 'RIGHT':
            self._rotate(key)

    def get_index(self, screen_x_res, screen_y_res):
        '''
        @param screen_x_res: Int x scaling
        @param screen_y_res: Int y scaling
        @screen_x/y_res both represent how many units each index represents.

        Determine the players index position in the environment array based on player's float x and y
        '''
        x_index = int(self.x // screen_x_res)
        y_index = int(self.y // screen_y_res)

        return x_index, y_index
