import numpy as np
import vector


# camera class
class Camera:
    camera_vars = np.zeros(10, dtype=int)

    # position, look_at,up,right are 3D vectors.
    # screen_d, screen_w are numbers.
    # x is an array of 10 integers.
    def __init__(self, position: np.ndarray, look_at: np.ndarray, up: np.ndarray, screen_d: float, screen_w: float):
        # Normalize Vectors from input.
        self.position = position
        self.look_at = vector.normalized(vector.minus(look_at, position))
        self.up = vector.normalized(vector.projected_left(up, self.look_at))
        self.screen_height = screen_d
        self.screen_width = screen_w
        self.right = vector.normalized(vector.cross_product(up, self.look_at))
