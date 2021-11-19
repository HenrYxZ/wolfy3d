import numpy as np


MAX_COLOR_VALUE = 255


def degrees2rads(angle):
    radians = (angle / 360) * 2 * np.pi
    return radians

def float2uint8(color):
    new_color = (MAX_COLOR_VALUE * color).round()
    return new_color