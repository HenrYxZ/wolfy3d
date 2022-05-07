import numpy as np
import pyglet
from pyglet.gl import *
from pyglet.window import key

# Local modules
from constants import COLOR_CHANNELS, TILE_SIZE, WALL_CODE
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
HEIGHT = 480
WIDTH = 640 + HEIGHT    # Adding a square for top view of size equal to height
IMG_FORMAT = 'RGB'
pitch = -WIDTH * COLOR_CHANNELS
# Image buffer
current_im_arr = np.zeros([HEIGHT, WIDTH, COLOR_CHANNELS], dtype=np.uint8)
data = current_im_arr.tobytes()
image_data = pyglet.image.ImageData(WIDTH, HEIGHT, IMG_FORMAT, data, pitch)


window = pyglet.window.Window(WIDTH, HEIGHT)
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()

level_map = LevelMap(MAP, TILE_SIZE)
level = Level("Lvl 1", level_map)
player_pos = Point(2.2, 3.3)
# rotation = math.pi / 3
rotation = 0
player = Player(player_pos, rotation)
tri_side = 20
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
player_sprite.rotation = np.rad2deg(-player.rot)
tiles = []
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
    player_sprite.position = np.array([player.pos.x, player.pos.y]) * top_ratio
    player_sprite.rotation = np.rad2deg(-player.rot)


def main():
    init_map_top()
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()


def init_map_top():
    current_map = current_scene.level.level_map.map_arr
    n, m = current_map.shape
    for j in range(n):
        for i in range(m):
            if current_map[j, i] == WALL_CODE:
                rec_size = HEIGHT / n
                x = i * rec_size
                y = j * rec_size
                tile = pyglet.shapes.Rectangle(
                    x, y, rec_size, rec_size, batch=batch
                )
                tiles.append(tile)


@window.event
def on_draw():
    global current_im_arr
    window.clear()
    render(current_scene, current_im_arr, FOV)
    # Transform image array to bytes data
    bytes_data = current_im_arr.tobytes()
    image_data.set_data(IMG_FORMAT, pitch, bytes_data)
    image_data.blit(480, 0)
    batch.draw()


if __name__ == '__main__':
    main()
