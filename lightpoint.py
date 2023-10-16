import numpy as np
import color


class LightPoint:
    # Position is a vector of size 3.
    # position = np.array()
    # color = Color()
    # specular = 0.0
    # shadow = 0.0
    # radius = 0.0

    def __init__(self, position: np.ndarray, inputColor: color.Color, specularity: float, shadow: float, radius: float):
        self.position = position
        self.color = inputColor
        self.specularity = specularity
        self.shadow = shadow
        self.radius = radius
