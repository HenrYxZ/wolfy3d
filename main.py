import numpy as np
import pyglet
from pyglet.gl import *


MAP = np.array([
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '1', '0', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '1', '1', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
    ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
])

# Game settings
WALL_HEIGHT = 2
TILE_SIZE = 1
FOV = 60
FPS = 17.5
# Screen settings
COLOR_CHANNELS = 3
WIDTH = 640
HEIGHT = 480
IMG_FORMAT = 'RGB'
pitch = -WIDTH * COLOR_CHANNELS
# Image buffer
im_arr = np.zeros([HEIGHT, WIDTH, COLOR_CHANNELS], dtype=np.uint8)
data = im_arr.tobytes()
image_data = pyglet.image.ImageData(WIDTH, HEIGHT, IMG_FORMAT, data, pitch)

window = pyglet.window.Window(WIDTH, HEIGHT)
color_timer = 0
blue = True
threshold = 3


def update(dt):
    global blue, im_arr, color_timer
    color_timer += dt
    if color_timer > threshold:
        color_timer = 0
        print("Changing color")
        if blue:
            im_arr = np.ones([WIDTH, HEIGHT, COLOR_CHANNELS], dtype=np.uint8)
            im_arr = im_arr * np.array([0, 0, 255], dtype=np.uint8)
            blue = False
        else:
            im_arr = np.zeros([WIDTH, HEIGHT, COLOR_CHANNELS], dtype=np.uint8)
            blue = True
    # Transform image array to bytes data
    data = im_arr.tobytes()
    image_data.set_data(IMG_FORMAT, pitch, data)
    pass


def main():
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()


@window.event
def on_draw():
    window.clear()
    image_data.blit(0, 0)


if __name__ == '__main__':
    main()
