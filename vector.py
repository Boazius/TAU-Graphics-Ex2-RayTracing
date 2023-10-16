from numpy import linalg as LNG
import numpy as np


def vector_len(v: np.ndarray):
    return LNG.norm(v)


def normalized(v: np.ndarray):
    norma = LNG.norm(v)
    ret_val = divide(v, norma)
    return ret_val


def divide(v, scalar):
    return np.divide(v, scalar)


def multiply(v, scalar):
    return np.multiply(v, scalar)


def minus(v: np.ndarray, other: np.ndarray):
    return np.subtract(v, other)


def add(v, other):
    return np.add(v, other)


def dot_product(v, other):
    if not isinstance(other, np.ndarray):
        other = np.array(other)

    other = other.reshape(3)
    v = v.reshape(3)
    return np.dot(v, other)


def cross_product(v, other):
    return np.cross(v, other)


def negative(v):
    return np.negative(v)


def projected(v, other):
    return multiply(normalized(other), dot_product(v, other) / vector_len(other))


def projected_left(v, other):
    return minus(v, projected(v, other))


def reflect(v1, other: np.ndarray):
    v = normalized(other)
    return minus(v1, multiply(v, 2 * dot_product(v1, v)))


def some_perpendicular(v):
    return normalized(cross_product(v, np.add(v, 7)))
