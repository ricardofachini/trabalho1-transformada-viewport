import numpy as np
from math import sin, cos, radians

ROTATION_ANGLE = 12
TRANSLATION_STEP = 20

rad = radians(ROTATION_ANGLE)
ROTATION_RIGHT = np.array([[cos(rad), -sin(rad), 0], [sin(rad), cos(rad), 0], [0, 0, 1]])

rad = -rad
ROTATION_LEFT  = np.array([[cos(rad), -sin(rad), 0], [sin(rad), cos(rad), 0], [0, 0, 1]])
