import material


class Shape:
    """
    Base class for representing different shapes in the scene.

    Attributes:
        material (material.Material): The material associated with the shape.
    """

    def __init__(self, inputMaterial: material.Material):
        """
        Initialize the Shape with the provided material.

        Args:
            inputMaterial (material.Material): The material associated with the shape.
        """
        self.material = inputMaterial
