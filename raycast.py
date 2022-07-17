import math
import numpy as np

import utils


class Ray:
    def __init__(self, pr, nr):
        self.pr = pr
        self.nr = nr

    @staticmethod
    def hit(level_map, current_tile):
        """
        Calculate if the given tile is a hit point for the ray or not

        Args:
            level_map (LevelMap): The tile map for the game
            current_tile (ndarray): 2D position for the given tile

        Returns:
            bool: whether the ray hit a wall for the given position or not
        """
        if current_tile[0] < 0 or current_tile[0] == (level_map.w - 1):
            return True
        elif current_tile[1] < 0 or current_tile[1] == (level_map.h - 1):
            return True
        if level_map.map_arr[current_tile[1], current_tile[0]]:
            return True
        return False

    def intersect(self, level_map):
        """
        Use DDA to find collision of ray with an object
        (using the algorithm from "Super Fast Ray Casting in Tiled Worlds using
        DDA" by javidx9 on YouTube).

        Args:
           level_map(LevelMap): Map for current level

        Returns:
           float: Distance from the ray starting point to nearest collider
        """
        # distance in an axis when the other axis distance is 1
        normalized_pos = self.pr / level_map.tile_size
        current_tile = (np.floor(normalized_pos)).astype(int)
        if self.nr[0] == 0:
            dx = float("inf")
        else:
            dx = math.sqrt(1 + (self.nr[1] / self.nr[0]) ** 2)
        if self.nr[1] == 0:
            dy = float("inf")
        else:
            dy = math.sqrt(1 + (self.nr[0] / self.nr[1]) ** 2)
        step_x = 1 if self.nr[0] > 0 else -1
        step_y = 1 if self.nr[1] > 0 else -1
        # length to the next intersection after adding 1 to x
        if self.nr[0] > 0:
            next_x = ((current_tile[0] + 1) - normalized_pos[0]) * dx
        else:
            next_x = (normalized_pos[0] - current_tile[0]) * dx
        if self.nr[1] > 0:
            next_y = ((current_tile[1] + 1) - normalized_pos[1]) * dy
        else:
            next_y = (normalized_pos[1] - current_tile[1]) * dy
        distance = 0
        while not self.hit(level_map, current_tile):
            if next_x < next_y:
                current_tile[0] += step_x
                distance = next_x
                next_x += dx
            else:
                current_tile[1] += step_y
                distance = next_y
                next_y += dy
        return distance


def raycast(player, current_angle, level_map):
    """
    Create a ray from the player view and intersect with the nearest collider
    Args:
        player (Player): Player object
        current_angle (float): Current angle in radians
        level_map (LevelMap): Map for current level

    Returns:
        float: Distance from the ray starting point to nearest hit
    """
    angle = current_angle + player.rot
    direction = utils.normalize(
        np.array([math.cos(angle), math.sin(angle)])
    )
    ray = Ray(player.pos.to_ndarray(), direction)
    distance = ray.intersect(level_map)
    return distance
