'''
This module implements the minimap class which tracks top down movement of player and direction player is facing
'''
from typing import List

class MiniMap(object):
    def __init__(self, env_array: List[str]) -> None:
        '''
        @attribute env_array: list of row strings representing map
        @attribute arrow_angle: Player facing angle constrained to 0 - 360
        @attribute current_arrow: Current directional indicator for player facing direction
        '''
        self.env_array = env_array
        self.arrow_angle = 0
        self.current_arrow = '>'

    def get_directional_indicator(self, angle: int) -> str:
        '''
        @param angle: Int Player facing angle

        Return current directional indicator for player
        '''
        if angle > 0:
            arrow_angle = angle % 360
        else:
            arrow_angle = angle * -1
            arrow_angle = angle % 360
            arrow_angle *= -1

        self.arrow_angle = arrow_angle

        if arrow_angle < -45 and arrow_angle > -135:
            self.current_arrow = '^'
        elif arrow_angle < -135 and arrow_angle > -225:
            self.current_arrow = '<'
        elif arrow_angle < -225 and arrow_angle > -315:
            self.current_arrow = 'v'
        elif arrow_angle < -315:
            self.current_arrow = '>'

        elif arrow_angle > -45 and arrow_angle < 45:
            self.current_arrow = '>'
        elif arrow_angle > 45 and arrow_angle < 135:
            self.current_arrow = 'v'
        elif arrow_angle > 135 and arrow_angle < 225:
            self.current_arrow = '<'
        elif arrow_angle > 225:
            self.current_arrow = '^'

        return self.current_arrow

    def get_minimap(self, x_index: int, y_index: int, angle: int) -> bytes:
        '''
        @param x_index: Int players x index within map_env_array
        @param y_idnex: Int players y index within map env_array
        @param angle: Int player facing direction

        Return bytes of minimap
        '''
        current_arrow = self.get_directional_indicator(angle)

        # Display player on map
        player_cord_x, player_cord_y = x_index, y_index
        map_env_array = self.env_array.copy()

        map_env_array[player_cord_y] = (map_env_array[player_cord_y][:player_cord_x] +
        'P' +
        map_env_array[player_cord_y][player_cord_x + 1:])

        # place directional arrow
        if current_arrow == '>':
            map_env_array[player_cord_y] = (map_env_array[player_cord_y][:player_cord_x+1] +
            current_arrow +
            map_env_array[player_cord_y][player_cord_x + 2:])
        elif current_arrow == '<':
            map_env_array[player_cord_y] = (map_env_array[player_cord_y][:player_cord_x-1] +
            current_arrow +
            map_env_array[player_cord_y][player_cord_x:])
        elif current_arrow == '^':
            map_env_array[player_cord_y-1] = (map_env_array[player_cord_y-1][:player_cord_x] +
            current_arrow +
            map_env_array[player_cord_y-1][player_cord_x + 1:])
        elif current_arrow == 'v':
            map_env_array[player_cord_y+1] = (map_env_array[player_cord_y+1][:player_cord_x] +
            current_arrow +
            map_env_array[player_cord_y+1][player_cord_x + 1:])

        map_env_string = '\n'.join(map_env_array)
        map_bytes = bytes(map_env_string, 'utf-8')

        return map_bytes
