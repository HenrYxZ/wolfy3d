import numpy as np


MAX_COLOR_VALUE = 255


def degrees2rads(angle):
    radians = (angle / 360) * 2 * np.pi
    return radians


def float2uint8(color):
    new_color = (MAX_COLOR_VALUE * color).round()
    return new_color

def lerp(t, a, b):
    return b * t + a * (1 - t)

def normalize(arr):
    """
    Normalize a vector using numpy.
    Args:
        arr (ndarray): Input vector
    Returns:
        ndarray: Normalized input vector
    """
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm
