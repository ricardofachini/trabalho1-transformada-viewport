import numpy as np
from math import sin, cos, radians

BORDER_SIZE = 20

ROTATION_ANGLE   = 12
TRANSLATION_STEP = 20
ZOOM_IN_SCALE    = 1.1
ZOOM_OUT_SCALE   = 0.9

rad = radians(ROTATION_ANGLE)
ROTATION_RIGHT = np.array([[cos(rad), -sin(rad), 0], [sin(rad), cos(rad), 0], [0, 0, 1]])

rad = -rad
ROTATION_LEFT  = np.array([[cos(rad), -sin(rad), 0], [sin(rad), cos(rad), 0], [0, 0, 1]])

# Characteristic Matrix (Bezier)
C_MATRIX = np.array([[ 1,  0,  0, 0],
                     [-3,  3,  0, 0],
                     [ 3, -6,  3, 0],
                     [-1,  3, -3, 1]])

M_BS = np.array([[-1/6, 1/2, -1/2, 1/6],
                 [ 1/2,  -1,  1/2, 0],
                 [-1/2,   0,  1/2, 0],
                 [ 1/6, 2/3,  1/6, 0]])
