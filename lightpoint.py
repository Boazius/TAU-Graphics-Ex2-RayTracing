import numpy as np
import color


class LightPoint:
    """
    Class representing a light source in a 3D space.

    Attributes:
        position (np.ndarray): The position of the light source.
        color (color.Color): The color of the light source.
        specularity (float): The specularity of the light source.
        shadow (float): The shadow value of the light source.
        radius (float): The radius of the light source.
    """

    def __init__(self, position: np.ndarray, input_color: color.Color, specularity: float, shadow: float, radius: float):
        """
        Initialize a LightPoint object with the given parameters.

        Args:
            position (np.ndarray): The position of the light source.
            input_color (color.Color): The color of the light source.
            specularity (float): The specularity of the light source.
            shadow (float): The shadow value of the light source.
            radius (float): The radius of the light source.
        """
        self.position = position
        self.color = input_color
        self.specularity = specularity
        self.shadow = shadow
        self.radius = radius
