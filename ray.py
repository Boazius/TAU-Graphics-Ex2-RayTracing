import numpy as np


class Ray:
    def __init__(self, start_point: np.ndarray, direction: np.ndarray):
        self.direction = direction
        self.start_point = start_point
