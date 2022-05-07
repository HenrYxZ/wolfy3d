import numpy as np


class Ray:
    def __init__(self, pr, nr):
        self.pr = pr
        self.nr = nr

    def get_distance(self, i, j, level_map):
        # calculate four points with x in the two sides and y in the upper
        # and bottom limit
        x0 = i * level_map.tile_size
        x1 = (i + 1) * level_map.tile_size
        y2 = j * level_map.tile_size
        y3 = (j + 1) * level_map.tile_size

    def intersect(self, level_map):
        """
        Use bresenham algorithm to find collision of ray with a wall
        Args:
           level_map(LevelMap): Map for current level

        Returns:
           float: Distance from the ray starting point to nearest wall
        """
        p1 = self.pr
        # point x2 is just any point far enough to make the line have the
        # intersection
        s = max(level_map.hrzn_size, level_map.vert_size)
        p2 = p1 + s * self.nr
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        slope = abs(dy / dx)
        # Decision error value
        d = abs(dy) - abs(dx) / 2
        i0 = int(p1[0] // level_map.tile_size)
        j0 = level_map.h - 1 - int(p1[1] // level_map.tile_size)
        i1, j1 = i0, j0
        x_step = 1 if dx > 0 else -1
        y_step = 1 if dy > 0 else -1
        error_type_1 = abs(dy)
        error_type_2 = abs(dy) - abs(dx)
        if slope < 1:
            iterations = abs(int(dx))
            for i in range(iterations):
                i1 += x_step
                if d < 0:
                    # Only increment x
                    d += error_type_1
                else:
                    # Increment x and y
                    d += error_type_2
                    j1 += y_step
        else:
            iterations = abs(int(dy))
            for j in range(iterations):
                j1 += y_step
                if d < 0:
                    # Only increment y
                    d += error_type_1
                else:
                    d += error_type_2
                    i1 += x_step
        # now we have a pixel in line (i1, j1)
        distance = self.get_distance(i1, j1)
        if distance:
            return distance


def raycast(player, level_map):
    """
    Use bresenham algorithm to find collision of ray with a wall
    Args:
        player(Player):
        level_map(LevelMap): Map for current level

    Returns:
        float: Distance from the ray starting point to nearest wall
    """
    pass
