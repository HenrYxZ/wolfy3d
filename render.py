import math
import numpy as np

# Local modules
from constants import COLOR_CHANNELS, TILE_SIZE, WALL_CODE, WALL_HEIGHT
import utils


def intersect_t(
    pos, perp_pos, theta, map_arr, direction, perp_dir, limit, perp_limit,
    is_horiz
):
    next_pos = (pos // TILE_SIZE) * TILE_SIZE
    increment = direction * TILE_SIZE
    if increment < 0:
        next_pos += TILE_SIZE
    next_perp = perp_pos
    if is_horiz:
        h = perp_limit // TILE_SIZE
    else:
        h = limit // TILE_SIZE
    while 0 < next_pos < limit:
        next_pos += increment
        diff_pos = abs(next_pos - pos)
        diff_perp = math.tan(theta) * diff_pos
        next_perp += perp_dir * diff_perp
        if next_perp < 0 or next_perp > perp_limit:
            return math.inf
        if is_horiz:
            i = int(next_pos // TILE_SIZE)
            j = int(h - 1 - next_perp // TILE_SIZE)
        else:
            i = int(next_perp // TILE_SIZE)
            j = int(h - 1 - next_pos // TILE_SIZE)
        if map_arr[j, i] == WALL_CODE:
            d = math.sqrt(diff_pos ** 2 + diff_perp ** 2)
            return d
    return limit


def intersect_x(pos, theta, map_arr, horizontal_dir, vertical_dir):
    h, w = map_arr.shape
    limit = w * TILE_SIZE
    perp_limit = h * TILE_SIZE
    is_horiz = True
    d = intersect_t(
        pos.x, pos.y, theta, map_arr, horizontal_dir, vertical_dir, limit,
        perp_limit, is_horiz
    )
    return d


def intersect_y(pos, theta, map_arr, horizontal_dir, vertical_dir):
    h, w = map_arr.shape
    limit = h * TILE_SIZE
    perp_limit = w * TILE_SIZE
    is_horiz = False
    d = intersect_t(
        pos.y, pos.x, theta, map_arr, vertical_dir, horizontal_dir, limit,
        perp_limit, is_horiz
    )
    return d


def intersect(pos, angle, map_arr):
    pi = math.pi
    if angle == 0:
        dx = intersect_x(pos, angle, map_arr, TILE_SIZE, 0)
        return dx
    elif angle == pi:
        dx = intersect_x(pos, angle, map_arr, -TILE_SIZE, 0)
        return dx
    elif angle < pi / 2:
        theta = angle
        horizontal_dir = 1
        vertical_dir = 1
    elif angle < pi:
        theta = pi - angle
        horizontal_dir = -1
        vertical_dir = 1
    elif angle < 3 * pi / 2:
        theta = angle - pi
        horizontal_dir = -1
        vertical_dir = -1
    else:
        theta = 2 * pi - angle
        horizontal_dir = 1
        vertical_dir = -1
    dx = intersect_x(pos, theta, map_arr, horizontal_dir, vertical_dir)
    dy = intersect_y(pos, theta, map_arr, horizontal_dir, vertical_dir)
    d = min(dx, dy)
    return d


def render(scene, im_arr, fov):
    """
    Render the scene in the given image array with the given field of view.
    Args:
        scene(Scene): The current scene of the game
        im_arr(ndarray): 2D RGB image in np.uint8
        fov(int): Field of view of the camera
    """
    height, width, color_channels = im_arr.shape
    im_arr[:, :] = np.zeros(color_channels, dtype=np.uint8)
    player = scene.player
    map_arr = scene.level.level_map.map_arr
    # if player is outside the map through error
    if not player.is_inside(scene.level.level_map):
        raise Exception("Player is outside of the map!")
    # Get player angle
    fov_in_rads = utils.degrees2rads(fov)
    current_angle = scene.player.rot - fov_in_rads / 2
    increment = fov_in_rads / width
    # Iterate rays for each horizontal pixel
    for i in range(width):
        d = intersect(player.pos, current_angle, map_arr)
        # color for the wall
        color = np.ones(COLOR_CHANNELS) / d
        # At one meter distance, a wall uses "height" pixels, calculate the
        # number of pixels at distance d
        h_pix = int(round((WALL_HEIGHT / d) * height))
        y_start = (height - h_pix) // 2
        rgb_color = utils.float2uint8(color)
        im_arr[y_start:-y_start, i] = rgb_color
        current_angle += increment
