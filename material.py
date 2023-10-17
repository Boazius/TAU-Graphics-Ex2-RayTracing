import color


class Material:
    """
    Class representing a material in a 3D space.

    Attributes:
        diffusion (color.Color): The diffusion color of the material.
        specularity (color.Color): The specularity color of the material.
        reflection (color.Color): The reflection color of the material.
        phong (float): The Phong value of the material.
        transparency (float): The transparency value of the material.
    """

    def __init__(self, diffusion: color.Color, specularity: color.Color, reflection: color.Color, phong: float, transparency: float):
        """
        Initialize a Material object with the given parameters.

        Args:
            diffusion (color.Color): The diffusion color of the material.
            specularity (color.Color): The specularity color of the material.
            reflection (color.Color): The reflection color of the material.
            phong (float): The Phong value of the material.
            transparency (float): The transparency value of the material.
        """
        self.diffusion = diffusion
        self.specularity = specularity
        self.reflection = reflection
        self.phong = phong
        self.transparency = transparency
