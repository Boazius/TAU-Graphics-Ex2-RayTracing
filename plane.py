import numpy as np
import vector
import intersection
import material
import shape
import ray


class Plane(shape.Shape):
    def __init__(self, normal: np.ndarray, offset: float, inputMaterial: material.Material):
        shape.Shape.__init__(self, inputMaterial)
        self.normal = vector.normalized(normal)
        self.offset = offset

    def intersect(self, inputRay: ray.Ray, shadow: bool):
        direction_dot_product = vector.dot_product(inputRay.direction, self.normal)
        if abs(direction_dot_product) < 0.01:
            return
        start_dot_product = vector.dot_product(inputRay.start_point, self.normal)
        t = (self.offset - start_dot_product) / direction_dot_product

        if t <= 0 or np.isnan(t):
            return

        intersection_point = vector.add(inputRay.start_point, vector.multiply(inputRay.direction, t))
        dist = pow(vector.vector_len(vector.minus(intersection_point, inputRay.start_point)), 2)

        if dist < 0.01:
            return

        intersection_normal = vector.multiply(self.normal, -direction_dot_product)

        return intersection.Intersection(intersection_point, intersection_normal, inputRay.direction, self.material)
