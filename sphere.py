import material
import vector
import shape
import math
import intersection
import numpy as np
import shape
import material
import ray


class Sphere(shape.Shape):
    # center = vector()
    # radius = 0.0
    # radius_sq = 0.0

    def __init__(self, center: np.ndarray, radius: float, inputMaterial: material.Material):
        shape.Shape.__init__(self, inputMaterial)
        self.center = center
        self.radius = radius
        self.radius_sq = radius * radius

    def intersect(self, inputRay: ray.Ray, shadow: bool):
        currVector = vector.minus(self.center, inputRay.start_point)
        tca = vector.dot_product(currVector, inputRay.direction)
        if tca < 0:
            return
        norm_vector = vector.dot_product(currVector, currVector)
        dist_squared = norm_vector - (tca * tca)
        if dist_squared > self.radius_sq:
            return
        if norm_vector < self.radius_sq:
            if shadow:
                return intersection.Intersection(inputRay.start_point, vector.negative(vector.normalized(currVector)),
                                                 inputRay.direction, self.material)
            else:
                return

        thc = math.sqrt(self.radius_sq - dist_squared)
        inter_point = vector.add(inputRay.start_point, vector.multiply(inputRay.direction, tca - thc))
        inter_normal = vector.normalized(vector.minus(inter_point, self.center))
        return intersection.Intersection(inter_point, inter_normal, inputRay.direction, self.material)
