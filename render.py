import math
import numpy as np

# Local modules
from constants import COLOR_CHANNELS, TILE_SIZE_MTS, WALL_CODE, WALL_HEIGHT_MTS
from raycast import raycast
import utils


def render(scene, im_arr, fov, pixel_size):
    """
    Render the scene in the given image array with the given field of view.
    Args:
        scene(Scene): The current scene of the game
        im_arr(ndarray): 2D RGB image in np.uint8
        fov(int): Field of view of the camera
        pixel_size (int): Size of each line segment
    """
    height, width, color_channels = im_arr.shape
    im_arr[:, :] = np.zeros(color_channels, dtype=np.uint8)
    # if player is outside the map through error
    if not scene.player.is_inside(scene.level.level_map):
        raise Exception("Player is outside of the map!")

    # Iterate rays for each horizontal pixel
    fov_rads = np.deg2rad(fov)
    for i in range(width // pixel_size):
        col = i * pixel_size
        current_angle = utils.lerp(
            col / width, -fov_rads / 2, fov_rads / 2
        )
        d = raycast(scene.player, current_angle, scene.level.level_map)
        # avoid fish eye effect by using perspective projection
        persp_d = math.cos(current_angle) * d
        # color for the wall
        color = np.ones(COLOR_CHANNELS)
        # At one meter distance, a wall uses the entire screen height, calculate
        # the number of pixels at distance d
        wall_height_pixels = int(
            round((WALL_HEIGHT_MTS / persp_d) * height)
        )
        y_start = (height - wall_height_pixels) // 2
        rgb_color = utils.float2uint8(color)
        im_arr[y_start:-y_start, col:col+pixel_size] = rgb_color
