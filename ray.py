import numpy as np


class Ray:
    """
    Class representing a ray in a 3D space.

    Attributes:
        start_point (np.ndarray): The starting point of the ray.
        direction (np.ndarray): The direction of the ray.
    """

    def __init__(self, start_point: np.ndarray, direction: np.ndarray):
        """
        Initialize a Ray object with the given parameters.

        Args:
            start_point (np.ndarray): The starting point of the ray.
            direction (np.ndarray): The direction of the ray.
        """
        self.direction = direction
        self.start_point = start_point
