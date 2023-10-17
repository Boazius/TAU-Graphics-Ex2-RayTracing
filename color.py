import numpy as np

def clip_number(rgb_num):
    """
    Clips the input number to the range [0, 1].

    Args:
        rgb_num (float): The input number to be clipped.

    Returns:
        float: The clipped number in the range [0, 1].
    """
    return np.clip(rgb_num, 0, 1)


class Color:
    """
    Class representing a color in RGB format.

    Attributes:
        r (float): The red component of the color.
        g (float): The green component of the color.
        b (float): The blue component of the color.
    """

    def __init__(self, r: float, g: float, b: float):
        """
        Initialize a Color object with the given RGB values.

        Args:
            r (float): The red component of the color.
            g (float): The green component of the color.
            b (float): The blue component of the color.
        """
        self.r = clip_number(r)
        self.g = clip_number(g)
        self.b = clip_number(b)

    def add_color(self, other):
        """
        Add the components of two colors.

        Args:
            other (Color): The other Color object to add.

        Returns:
            Color: A new Color object with the summed RGB values.
        """
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def mult_color(self, other):
        """
        Multiply the components of two colors.

        Args:
            other (Color): The other Color object to multiply.

        Returns:
            Color: A new Color object with the multiplied RGB values.
        """
        return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def mult_scalar_color(self, scalar):
        """
        Multiply the components of the color by a scalar.

        Args:
            scalar (float): The scalar value to multiply with.

        Returns:
            Color: A new Color object with the multiplied RGB values.
        """
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)

    def grayscale_color(self):
        """
        Compute the grayscale value of the color.
        """
        out_sum = self.r + self.g + self.b
        return out_sum / 3
