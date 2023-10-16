import vector
import material
import numpy as np


class Intersection:
    # vectors will be np arrrays of size 3.
    # inter_point = np.array()
    # normal = np.array()
    # direction = np.array()
    # material = ?

    def __init__(self, inter_point: np.ndarray, normal: np.ndarray, direction: np.ndarray,
                 inputMaterial: material.Material):
        self.intersection_point = inter_point
        self.normal = normal
        self.direction = direction
        self.material = inputMaterial
