import math
import numpy as np


import utils


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_ndarray(self):
        arr = np.array([self.x, self.y])
        return arr


class Player:
    # speed in mt/s
    DEFAULT_SPEED = 1.42
    # turn speed takes 2 seconds to turn 360°
    DEFAULT_TURN_SPEED = (2 * math.pi) / 2
    DEFAULT_RADIUS = 1

    def __init__(
        self, position, rotation, speed=DEFAULT_SPEED,
        turn_speed=DEFAULT_TURN_SPEED, radius=DEFAULT_RADIUS
    ):
        self.pos = position
        self.rot = rotation
        self.speed = speed
        self.turn_speed = turn_speed
        self.radius = radius

    def is_inside(self, level_map):
        h, w = level_map.map_arr.shape
        if not 0 <= self.pos.x <= w * level_map.tile_size:
            return False
        if not 0 <= self.pos.y <= h * level_map.tile_size:
            return False
        return True

    def set_pos_to_bounds(self, level_map):
        # 1 mt is
        horizontal_limit = level_map.hrzn_size - self.radius
        vertical_limit = level_map.vert_size - self.radius
        if self.pos.x < self.radius:
            self.pos.x = self.radius
        elif self.pos.x > horizontal_limit:
            self.pos.x = horizontal_limit
        if self.pos.y < self.radius:
            self.pos.y = self.radius
        elif self.pos.y > vertical_limit:
            self.pos.y = vertical_limit

    def get_dx_and_dy(self, dt):
        dx = math.cos(self.rot) * self.speed * dt
        dy = math.sin(self.rot) * self.speed * dt
        return dx, dy

    def get_direction(self):
        direction = utils.normalize(
            np.array([math.cos(self.rot), math.sin(self.rot)])
        )
        return direction

    def get_position(self):
        position = self.pos.to_ndarray()
        return position

    def move_forward(self, dt, level_map):
        dx, dy = self.get_dx_and_dy(dt)
        self.pos.x += dx
        self.pos.y += dy
        self.set_pos_to_bounds(level_map)

    def move_backward(self, dt, level_map):
        dx, dy = self.get_dx_and_dy(dt)
        self.pos.x -= dx
        self.pos.y -= dy
        self.set_pos_to_bounds(level_map)

    def turn_left(self, dt):
        self.rot += self.turn_speed * dt
        if self.rot > 2 * math.pi:
            self.rot -= 2 * math.pi

    def turn_right(self, dt):
        self.rot -= self.turn_speed * dt
        if self.rot < 0:
            self.rot += 2 * math.pi


class LevelMap:
    def __init__(self, map_arr, tile_size):
        self.map_arr = np.flipud(map_arr)
        self.h, self.w = map_arr.shape
        self.tile_size = tile_size
        self.hrzn_size = self.w * self.tile_size
        self.vert_size = self.h * self.tile_size


class Level:
    def __init__(self, name, level_map):
        self.name = name
        self.level_map = level_map


class Scene:
    def __init__(self, player, level):
        self.player = player
        self.level = level


class Game:
    def __init__(self, scene):
        self.scene = scene
