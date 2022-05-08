import math
import numpy as np

import utils


class Ray:
    def __init__(self, pr, nr):
        self.pr = pr
        self.nr = nr

    @staticmethod
    def finished(level_map, current_tile):
        if current_tile[0] < 0 or current_tile[0] > level_map.w:
            return True
        elif current_tile[1] < 0 or current_tile[1] > level_map.h:
            return True
        if level_map.map_arr[current_tile]:
            return True

    def intersect(self, level_map):
        """
        Use DDA to find collision of ray with an object
        Args:
           level_map(LevelMap): Map for current level

        Returns:
           float: Distance from the ray starting point to nearest collider
        """
        # distance in an axis when the other axis distance is 1
        normalized_pos = self.pr / level_map.tile_size
        current_tile = (np.floor(normalized_pos)).astype(int)
        dx = sqrt(1 + (self.nr[1] / self.nr[0]) ** 2)
        dy = sqrt(1 + (self.nr[0] / self.nr[1]) ** 2)
        step_x = 1 if self.nr[0] > 0 else -1
        step_y = 1 if self.nr[1] > 0 else -1
        # length to the next intersection after adding 1 to x
        if self.nr[0] > 0:
            next_x = ((current_tile[0] + 1) - normalized_pos[0]) * dy
        else:
            next_x = (normalized_pos[0] - current_tile[0]) * dy
        if self.nr[1] > 0:
            next_y = ((current_tile[1] + 1) - normalized_pos[1]) * dx
        else:
            next_y = (normalized_pos[1] - current_tile[1]) * dx
        distance = 0
        while not self.finished(level_map, current_tile):
            if next_x < next_y:
                current_tile[0] += step_x
                distance = next_x
                next_x += dy
            else:
                current_tile[1] += step_y
                distance = next_y
                next_y += dx
        return distance


def raycast(player, level_map):
    """
    Create a ray from the player view and intersect with the nearest collider
    Args:
        player(Player): Player object
        level_map(LevelMap): Map for current level

    Returns:
        float: Distance from the ray starting point to nearest wall
    """
    direction = utils.normalize(
        np.array([math.cos(player.rot), math.sin(player.rot)])
    )
    ray = Ray(player.pos, direction)
    distance = ray.intersect(level_map)
    return distance
