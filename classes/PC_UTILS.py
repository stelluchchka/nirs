import numpy as np
import pprint
from time import time
from pypcd import pypcd
import math

class PC_UTILS:
    def shift(points, x, y, z):
        """ Return shifted data
        Input:
            points: origin data
            x, y, z: shift values along the X, Y and Z axes, respectively.
        Return:
            points + shift_matrix: shifted data
        """
        x_shift = np.full((points.shape[0],1), x)
        y_shift = np.full((points.shape[0],1), y)
        z_shift = np.full((points.shape[0],1), z)
        if points.shape[1] == 3:
            shift_matrix = np.concatenate([x_shift, y_shift, z_shift], axis=1)
        elif points.shape[1] == 2:
            shift_matrix = np.concatenate([x_shift, y_shift], axis=1)
        elif points.shape[1] == 1:
            shift_matrix = np.concatenate([x_shift], axis=1)
        return points + shift_matrix
    
    def rotate_points(points, rotation_angle):
        """ Return rotated data
        Input:
            points: origin data
            rotation_angle: rotation angle in radians
        Return:
            rotated_points: rotated data
        """
        rotated_points = []
        for point in points:
            xp = math.cos(rotation_angle) * point[0] - math.sin(rotation_angle) * point[1]
            yp = math.sin(rotation_angle) * point[0] + math.cos(rotation_angle) * point[1]
            rotated_points.append([xp, yp, point[2]])
        return rotated_points
