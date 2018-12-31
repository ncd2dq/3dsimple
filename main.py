#Microsoft Visual C/C++ Runtime
import msvcrt
import os
import time
import sys
import math


def get_keys():
    '''
    Asynchronous callback if key is pressed
    '''
    if msvcrt.kbhit():
        key = msvcrt.getch()

        if key == b'H':
            return 'UP'
        elif key == b'M':
            return 'RIGHT'
        elif key == b'P':
            return 'DOWN'
        elif key == b'K':
            return 'LEFT'
        elif key == b'q':
            return 'QUIT'
        else:
            return False
    return False


def test_performance(env):
    import numpy as np
    #print string vs print array
    chars = ''.join(env)
    chars = bytes(chars, 'utf-8')
    a_chars = env
    np_chars = np.array(env)

    str_total = 0 
    a_total = 0
    np_total = 0

    trials = 1000

    for i in range(trials):
        print('\rFull String------', end='')
        before = time.time()
        #os.system('cls')
        #print(chars, end='\r')
        sys.stdout.buffer.write(chars)
        after = time.time()
        str_total += after - before

        '''
        print('\rBoring Array------', end='')
        before = time.time()
        #os.system('cls')
        print(a_chars, end='')
        after = time.time()
        a_total += after - before

        print('\rNumpy Array------')
        before = time.time()
        #os.system('cls')
        print(np_chars, end='')
        after = time.time()
        np_total += after - before
        '''

    str_total /= trials
    a_total /= trials
    np_total /= trials

    print(str_total)
    print(a_total)
    print(np_total)

    #Best performance was python array, string/numpy are relatively close
    #os.system('cls') reduces run time to 0.02 (50fps) for all versions


def create_env():
    '''
    Create blueprint floorplan of environment
    '''
    env_array = [
            '############',
            '#..........#',
            '#..........#',
            '#..........#',
            '#..........#',
            '#..........#',
            '#..#########',
            '##.......###',
            '##..###...##',
            '#..####..###',
            '#.##.##....#',
            '#.##.##..###',
            '#....##....#',
            '#######..#.#',
            '##...##.##.#',
            '##.........#',
            '##.......###',
            '############',
    ]

    env_string = ''.join(env_array)

    return env_array, env_string


def create_textures():
    '''
    Transform unicode string literals into byte code: b'\xe2\x96\x93' that can be read by the stdout buffer
    '''
    texture_byte_map = {
        'light_shade': bytes('░','utf-8'),
        'medium_shade': bytes('▒','utf-8'),
        'dark_shade': bytes('▓','utf-8'),
        'full_shade': bytes('█', 'utf-8'),
        'floor_close': bytes('▃', 'utf-8'),
        'floor_medium': bytes('▂', 'utf-8'),
        'floor_far': bytes('▁', 'utf-8'),
        'ceiling_close': bytes('#', 'utf-8'),
        'ceiling_medium': bytes('x', 'utf-8'),
        'ceiling_far': bytes('.', 'utf-8'),
    }

    texture_byte_map = {
        'light_shade': '░',
        'medium_shade': '▒',
        'dark_shade': '▓',
        'full_shade': '█', 
        'floor_close': '▃', 
        'floor_medium': '▂', 
        'floor_far': '▁', 
        'ceiling_close': '#', 
        'ceiling_medium': 'x', 
        'ceiling_far': '.', 
    }

    return texture_byte_map


def generate_player_vision(distances, texture_map, max_distance):
    '''
    @param distances:: Python array of floating point distances between rays and walls

    Generate a string that represents the players vision. Note, each element in the array
    represents a column on the screen.

    Legal:
    a = b'xxxxx---...' + bytes('▓', 'utf-8')
    '''
    to_transpose = 'h' + texture_map['light_shade'] + '\n' + 'i' + texture_map['light_shade'] + '\n'

    # NEED TO GENERATE OUTPUT AND TRANSPOSE COLUMNS
    for distance in distances:
        pass


    transposed = ''.join([''.join(i) for i in zip(*to_transpose.split())])
    transposed = bytes(transposed, 'utf-8')
    return transposed


def main(env_array, env_string, texture_map, wall='#'):
    env_string = bytes(env_string, 'utf-8')
    last_key = None

    # If resolution is 12, each 3D column will be 12 units long
    env_index_width = len(env_array[0])
    env_index_height = len(env_array)
    screen_width_resolution = 12
    screen_height_resolution = 12
    screen_width = env_index_width * screen_width_resolution
    screen_height = env_index_height * screen_height_resolution

    # Player Attributes (Angles in Degrees)
    player_visual_field_breadth = 90
    playerX = 24.0
    playerY = 12.0
    playerMoveSpeed = 2
    playerTurnSpeed = 5
    playerAngle = 0

    while last_key != 'QUIT':
        new_key = get_keys()

        #
        # PLAYER MOVEMENT
        #
        # Move player in direction they are facing
        if new_key == 'UP' or new_key == 'DOWN':
            # Determine amount of x / y component in direction player is facing
            angle_radians = math.radians(playerAngle)
            increment_x = math.cos(angle_radians) * playerMoveSpeed
            increment_y = math.sin(angle_radians) * playerMoveSpeed
            if new_key == 'UP':   
                playerX += increment_x
                playerY += increment_y
            else:
                playerX -= increment_x
                playerY -= increment_y
        # Rotate characters visual field
        if new_key == 'LEFT':
            playerAngle += playerTurnSpeed
        elif new_key == 'RIGHT':
            playerAngle -= playerTurnSpeed

        #
        # RAY TRACING
        #
        # Determine distances to objects in player field
        # each distance until ray touched an object will determine 1 full column drawn
        distances = []
        ray_count = 120
        ray_angle_incrementation = player_visual_field_breadth / ray_count
        ray_distance_incrementation = 2
        ray_max_dist = screen_width
        for ray_num in range(ray_count):
            ray_x = playerX
            ray_y = playerY
            ray_angle = (
                            playerAngle
                            - (player_visual_field_breadth / 2)
                            + (ray_angle_incrementation * ray_num)
                        )

            # Increment the rays length until a collision
            while True:
                ray_index_x = int(ray_x // screen_width_resolution)
                ray_index_y = int(ray_y // screen_height_resolution)
                ray_distance = 0

                # If we hit a wall, determine distance we traveled
                if ray_distance >= ray_max_dist:
                    distances.append(ray_distance)
                    break
                elif env_array[ray_index_y][ray_index_x] == wall:
                    distances.append(ray_distance)
                    break
                else:
                    ray_distance += ray_distance_incrementation
                    ray_angle_radians = math.radians(ray_angle)
                    ray_x += math.cos(ray_angle_radians) * ray_distance
                    ray_y += math.sin(ray_angle_radians) * ray_distance

        #
        # SCREEN RENDERING
        #
        # Now we have an array of distances (@array distances) for each array
        # each distance in the array represents a column
        player_vision = generate_player_vision(distances, texture_map, ray_max_dist)
        last_key = new_key
        sys.stdout.buffer.write(player_vision)
        sys.stdout.flush()


if __name__ == '__main__':
    env_array, env_string = create_env()
    texture_map = create_textures()
    main(env_array, env_string, texture_map)
    
    # for i in range(5):
    #     vart = bytes(str(i), 'utf-8')
    #     sys.stdout.buffer.write(vart)
    #     sys.stdout.flush() # Flush forces the buffer to screen
    #     time.sleep(1)
    input('Press <Enter> to quit')