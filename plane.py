import numpy as np
import vector
import intersection
import material
import shape
import ray


class Plane(shape.Shape):
    """
    Class representing a plane shape in a 3D space.

    Attributes:
        normal (np.ndarray): The normal vector of the plane.
        offset (float): The offset value of the plane.
    """

    def __init__(self, normal: np.ndarray, offset: float, input_material: material.Material):
        """
        Initialize a Plane object with the given parameters.

        Args:
            normal (np.ndarray): The normal vector of the plane.
            offset (float): The offset value of the plane.
            input_material (material.Material): The material of the plane.
        """
        shape.Shape.__init__(self, input_material)
        self.normal = vector.normalized(normal)
        self.offset = offset

    def intersect(self, input_ray: ray.Ray, shadow: bool):
        """
        Compute the intersection of the plane with the input ray.

        Args:
            input_ray (ray.Ray): The input ray to check for intersection.
            shadow (bool): A boolean indicating if the plane is a shadow or not.

        Returns:
            intersection.Intersection or None: An Intersection object if there is an intersection, None otherwise.
        """
        direction_dot_product = vector.dot_product(input_ray.direction, self.normal)

        if abs(direction_dot_product) < 0.01:
            return

        start_dot_product = vector.dot_product(input_ray.start_point, self.normal)
        t = (self.offset - start_dot_product) / direction_dot_product

        if t <= 0 or np.isnan(t):
            return

        intersection_point = vector.add(input_ray.start_point, vector.multiply(input_ray.direction, t))
        dist = pow(vector.vector_len(vector.minus(intersection_point, input_ray.start_point)), 2)

        if dist < 0.01:
            return

        intersection_normal = vector.multiply(self.normal, -direction_dot_product)

        return intersection.Intersection(intersection_point, intersection_normal, input_ray.direction, self.material)
