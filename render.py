import math
import numpy as np

# Local modules
from constants import COLOR_CHANNELS, TILE_SIZE_MTS, WALL_CODE, WALL_HEIGHT_MTS
from raycast import raycast
import utils


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
    # if player is outside the map through error
    if not scene.player.is_inside(scene.level.level_map):
        raise Exception("Player is outside of the map!")

    distances = raycast(scene.player, scene.level.level_map, fov, width)
    # Iterate rays for each horizontal pixel
    for i in range(width):
        d = distances[i]
        # color for the wall
        color = np.ones(COLOR_CHANNELS)
        # At one meter distance, a wall uses the entire screen height, calculate
        # the number of pixels at distance d
        wall_height_pixels = int(round((WALL_HEIGHT_MTS / d) * height))
        y_start = (height - wall_height_pixels) // 2
        rgb_color = utils.float2uint8(color)
        im_arr[y_start:-y_start, i] = rgb_color
