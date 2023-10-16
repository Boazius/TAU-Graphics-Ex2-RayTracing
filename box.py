import numpy as np
import vector
import ray
import material
import sys
import intersection


# boxes class

class Box:

    def __init__(self, center: np.ndarray, half_scale: np.ndarray, input_material: material.Material):
        # Normalize Vectors from input.
        self.center = center
        self.half_scale = vector.multiply(half_scale, 0.5)
        self.material = input_material

    def intersect(self, inputRay: ray.Ray, shadow: bool):
        t_near = -float("inf")
        t_far = float("inf")
        offset_center = vector.minus(self.center, inputRay.start_point)
        axis = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        for i in range(3):
            r = offset_center.item(i)
            s = inputRay.direction.item(i)
            if abs(s) < sys.float_info.epsilon:
                t0 = r + self.half_scale.item(i)
                if t0 > 0:
                    t0 = float("inf")
                else:
                    t0 = -float("inf")
                t1 = r - self.half_scale.item(i)
                if t1 > 0:
                    t1 = float("inf")
                else:
                    t1 = -float("inf")
            else:
                t0 = (r + self.half_scale.item(i)) / s
                t1 = (r - self.half_scale.item(i)) / s
            if t0 > t1:
                tmp = t0
                t0 = t1
                t1 = tmp
            t_near = max(t_near, t0)
            t_far = min(t_far, t1)
            if t_near > t_far or t_far < 0:
                return None  # no intersection
        if t_near < 0:
            return None  # opposite direction

        intersection_point = vector.add(inputRay.start_point, vector.multiply(inputRay.direction, t_near))
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
        return intersection.Intersection(intersection_point, normal, inputRay.direction, self.material)
