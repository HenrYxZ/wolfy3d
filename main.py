import numpy as np
import pyglet
from pyglet.gl import *
from pyglet.window import key

# Local modules
from constants import COLOR_CHANNELS, TILE_SIZE
from game import *
from render import render

MAP = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
], dtype=np.uint8)

# Game settings

FOV = 60
FPS = 17.5
# Screen settings
WIDTH = 640
HEIGHT = 480
IMG_FORMAT = 'RGB'
pitch = -WIDTH * COLOR_CHANNELS
# Image buffer
current_im_arr = np.zeros([HEIGHT, WIDTH, COLOR_CHANNELS], dtype=np.uint8)
data = current_im_arr.tobytes()
image_data = pyglet.image.ImageData(WIDTH, HEIGHT, IMG_FORMAT, data, pitch)


window = pyglet.window.Window(WIDTH, HEIGHT)
keys = key.KeyStateHandler()
window.push_handlers(keys)

level_map = LevelMap(MAP, TILE_SIZE)
level = Level("Lvl 1", level_map)
player_pos = Position(2.2, 3.3)
rotation = math.pi / 3
player = Player(player_pos, rotation)
current_scene = Scene(player, level)


def update(dt):
    if keys[key.Q]:
        pyglet.app.exit()
    elif keys[key.W]:
        player.move_forward(dt, level_map)
    elif keys[key.S]:
        player.move_backward(dt, level_map)
    elif keys[key.A]:
        player.turn_left(dt)
    elif keys[key.D]:
        player.turn_right(dt)


def main():
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()


@window.event
def on_draw():
    global current_im_arr
    window.clear()
    render(current_scene, current_im_arr, FOV)
    # Transform image array to bytes data
    bytes_data = current_im_arr.tobytes()
    image_data.set_data(IMG_FORMAT, pitch, bytes_data)
    image_data.blit(0, 0)


if __name__ == '__main__':
    main()
