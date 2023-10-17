import numpy as np
import material


class Intersection:
    """
    Class representing an intersection point in a 3D space.

    Attributes:
        intersection_point (np.ndarray): The point of intersection.
        normal (np.ndarray): The normal vector at the intersection point.
        direction (np.ndarray): The direction of the intersection.
        material (material.Material): The material at the intersection point.
    """

    def __init__(self, inter_point: np.ndarray, normal: np.ndarray, direction: np.ndarray, input_material: material.Material):
        """
        Initialize an Intersection object with the given parameters.

        Args:
            inter_point (np.ndarray): The point of intersection.
            normal (np.ndarray): The normal vector at the intersection point.
            direction (np.ndarray): The direction of the intersection.
            input_material (material.Material): The material at the intersection point.
        """
        self.intersection_point = inter_point
        self.normal = normal
        self.direction = direction
        self.material = input_material
