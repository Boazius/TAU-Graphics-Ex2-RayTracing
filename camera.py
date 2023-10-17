import numpy as np
import vector


class Camera:
    """
    Class representing a camera in a 3D space.

    Attributes:
        position (np.ndarray): The position of the camera.
        look_at (np.ndarray): The direction the camera is looking at.
        up (np.ndarray): The up direction of the camera.
        screen_height (float): The height of the screen.
        screen_width (float): The width of the screen.
        right (np.ndarray): The vector representing the right direction of the camera.
    """

    def __init__(self, position: np.ndarray, look_at: np.ndarray, up: np.ndarray, screen_d: float, screen_w: float):
        """
        Initialize a Camera object with the given parameters.

        Args:
            position (np.ndarray): The position of the camera.
            look_at (np.ndarray): The direction the camera is looking at.
            up (np.ndarray): The up direction of the camera.
            screen_d (float): The distance from the camera to the screen.
            screen_w (float): The width of the screen.
        """
        self.position = position
        self.look_at = vector.normalized(vector.minus(look_at, position))
        self.up = vector.normalized(vector.projected_left(up, self.look_at))
        self.screen_height = screen_d
        self.screen_width = screen_w
        self.right = vector.normalized(vector.cross_product(up, self.look_at))
