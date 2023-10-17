import numpy as np
import vector
import ray
import material
import sys
import intersection


class Box:
    """
    Class representing a box in a 3D space.

    Attributes:
        center (np.ndarray): The center point of the box.
        half_scale (np.ndarray): Half of the length of each side of the box.
        material (material.Material): The material of the box.
    """

    def __init__(self, center: np.ndarray, half_scale: np.ndarray, input_material: material.Material):
        """
        Initialize a Box object with the given parameters.

        Args:
            center (np.ndarray): The center point of the box.
            half_scale (np.ndarray): Half of the length of each side of the box.
            input_material (material.Material): The material of the box.
        """
        self.center = center
        self.half_scale = vector.multiply(half_scale, 0.5)
        self.material = input_material

    def intersect(self, input_ray: ray.Ray, shadow: bool):
        """
        Compute intersection of the box with the input ray.

        Args:
            input_ray (ray.Ray): The input ray to check for intersection.
            shadow (bool): A boolean indicating if the box is a shadow or not.

        Returns:
            intersection.Intersection or None: An Intersection object if there is an intersection, None otherwise.
        """
        t_near = -float("inf")
        t_far = float("inf")
        offset_center = vector.minus(self.center, input_ray.start_point)
        axis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        for i in range(3):
            r = offset_center.item(i)
            s = input_ray.direction.item(i)

            if abs(s) < sys.float_info.epsilon:
                t0 = float("inf") if (r + self.half_scale.item(i)) > 0 else -float("inf")
                t1 = float("inf") if (r - self.half_scale.item(i)) > 0 else -float("inf")
            else:
                t0 = (r + self.half_scale.item(i)) / s
                t1 = (r - self.half_scale.item(i)) / s

            if t0 > t1:
                t0, t1 = t1, t0

            t_near = max(t_near, t0)
            t_far = min(t_far, t1)

            if t_near > t_far or t_far < 0:
                return None  # No intersection

        if t_near < 0:
            return None  # Opposite direction

        intersection_point = vector.add(input_ray.start_point, vector.multiply(input_ray.direction, t_near))
        pc = vector.minus(intersection_point, self.center)
        normal = None

        for i in range(3):
            b = axis[i, :3]
            if abs(pc.item(i) - self.half_scale.item(i)) <= sys.float_info.epsilon:
                normal = b
                break
            if abs(vector.dot_product(pc, b) + self.half_scale.item(i)) <= sys.float_info.epsilon:
                normal = vector.multiply(b, -1.0)
                break

        return intersection.Intersection(intersection_point, normal, input_ray.direction, self.material)
