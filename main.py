import math

import numpy as np
import pyglet
from pyglet.gl import *
from pyglet.shapes import Line
from pyglet.window import key

# Local modules
from constants import COLOR_CHANNELS, TILE_SIZE_MTS, WALL_CODE
from game import *
from raycast import raycast
from render import render
import utils


MAP = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
], dtype=np.uint8)

# Game settings

FOV = 60
FPS = 17.5
# Screen settings
HEIGHT = 480
WIDTH = 640
IMG_FORMAT = 'RGB'
pitch = -WIDTH * COLOR_CHANNELS
# Other settings
PIXEL_SIZE = 2
# Image buffer
current_im_arr = np.zeros([HEIGHT, WIDTH, COLOR_CHANNELS], dtype=np.uint8)
data = current_im_arr.tobytes()
image_data = pyglet.image.ImageData(WIDTH, HEIGHT, IMG_FORMAT, data, pitch)


window = pyglet.window.Window(WIDTH + HEIGHT, HEIGHT)   # Add space for debug
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()

level_map = LevelMap(MAP, TILE_SIZE_MTS)
level = Level("Lvl 1", level_map)
player_pos = Point(2.2, 3.3)
rotation = 0
player = Player(player_pos, rotation)
player_img = pyglet.image.load("player.png")
player_img.anchor_x = player_img.width // 2
player_img.anchor_y = player_img.height // 2
top_ratio = HEIGHT / level_map.hrzn_size
player_sprite = pyglet.sprite.Sprite(
    player_img,
    player_pos.x * top_ratio,
    player_pos.y * top_ratio,
    batch=batch
)
player_sprite.rotation = np.rad2deg(player.rot)
player_sprite.scale = (player_img.width / top_ratio) * (2 * player.radius)
tiles = []
current_scene = Scene(player, level)
debug_lines = []


def shoot_debug_ray():
    d = raycast(player, 0, current_scene.level.level_map)
    direction = player.get_direction()
    p1 = player.get_position() * top_ratio
    p2 = p1 + d * direction * top_ratio
    debug_line = debug_lines[0]
    debug_line.x = int(p1[0])
    debug_line.y = int(p1[1])
    debug_line.x2 = int(p2[0])
    debug_line.y2 = int(p2[1])


def update_debug_rays():
    fov_rads = np.deg2rad(FOV)
    for i in range(WIDTH):
        current_angle = utils.lerp(
            i / WIDTH, -fov_rads / 2, fov_rads / 2
        )
        d = raycast(player, current_angle, current_scene.level.level_map)
        angle = current_angle + player.rot
        direction = utils.normalize(
            np.array([math.cos(angle), math.sin(angle)])
        )
        p1 = player.pos.to_ndarray() * top_ratio
        p2 = p1 + d * direction * top_ratio
        debug_line = debug_lines[i]
        debug_line.x, debug_line.y = p1
        debug_line.x2, debug_line.y2 = p2


def update(dt):
    if keys[key.Q]:
        pyglet.app.exit()
    if keys[key.W]:
        player.move_forward(dt, level_map)
    if keys[key.S]:
        player.move_backward(dt, level_map)
    if keys[key.A]:
        player.turn_left(dt)
    if keys[key.D]:
        player.turn_right(dt)
    player_sprite.position = player.pos.to_ndarray() * top_ratio
    # use negative rotation because pyglet is counter-clockwise
    player_sprite.rotation = np.rad2deg(-player.rot)
    update_debug_rays()


def main():
    init_map_top()
    shoot_debug_ray()
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()


def init_map_top():
    # Initialize the top view
    current_map = current_scene.level.level_map.map_arr
    n, m = current_map.shape
    for j in range(n):
        for i in range(m):
            if current_map[j, i] == WALL_CODE:
                rec_size = HEIGHT / n
                x = i * rec_size
                y = j * rec_size
                # substract 1 pixel from rec_size so there's margin between
                # rectangles
                tile = pyglet.shapes.Rectangle(
                    x, y, rec_size - 1, rec_size - 1, batch=batch
                )
                tiles.append(tile)
    # create debugging green lines for top view
    for i in range(WIDTH):
        line = Line(0, 0, 0, 0, color=(0, 255, 0), batch=batch)
        line.opacity = 120
        debug_lines.append(line)


@window.event
def on_draw():
    global current_im_arr
    window.clear()
    render(current_scene, current_im_arr, FOV, PIXEL_SIZE)
    # Transform image array to bytes data
    current_im_arr = np.flipud(current_im_arr)
    bytes_data = current_im_arr.tobytes()
    image_data.set_data(IMG_FORMAT, pitch, bytes_data)
    image_data.blit(HEIGHT, 0)
    batch.draw()


if __name__ == '__main__':
    main()
