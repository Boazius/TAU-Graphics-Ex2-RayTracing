import numpy as np


def vector_len(v: np.ndarray) -> float:
    """
    Calculate the length of the vector.

    Args:
        v (np.ndarray): The input vector.

    Returns:
        float: The length of the vector.
    """
    return np.linalg.norm(v)


def normalized(v: np.ndarray) -> np.ndarray:
    """
    Normalize the input vector.

    Args:
        v (np.ndarray): The input vector.

    Returns:
        np.ndarray: The normalized vector.
    """
    norma = np.linalg.norm(v)
    ret_val = divide(v, norma)
    return ret_val


def divide(v, scalar):
    """
    Divide the vector by a scalar.

    Args:
        v: The vector.
        scalar: The scalar value to divide by.

    Returns:
        The divided vector.
    """
    return np.divide(v, scalar)


def multiply(v, scalar):
    """
    Multiply the vector by a scalar.

    Args:
        v: The vector.
        scalar: The scalar value to multiply by.

    Returns:
        The multiplied vector.
    """
    return np.multiply(v, scalar)


def minus(v: np.ndarray, other: np.ndarray) -> np.ndarray:
    """
    Subtract one vector from another.

    Args:
        v (np.ndarray): The first vector.
        other (np.ndarray): The second vector.

    Returns:
        np.ndarray: The resulting vector after subtraction.
    """
    return np.subtract(v, other)


def add(v, other):
    """
    Add one vector to another.

    Args:
        v: The first vector.
        other: The second vector.

    Returns:
        The resulting vector after addition.
    """
    return np.add(v, other)


def dot_product(v, other) -> float:
    """
    Calculate the dot product of two vectors.

    Args:
        v: The first vector.
        other: The second vector.

    Returns:
        The dot product of the two vectors.
    """
    if not isinstance(other, np.ndarray):
        other = np.array(other)

    other = other.reshape(3)
    v = v.reshape(3)
    return np.dot(v, other)


def cross_product(v, other):
    """
    Calculate the cross product of two vectors.

    Args:
        v: The first vector.
        other: The second vector.

    Returns:
        The cross product of the two vectors.
    """
    return np.cross(v, other)


def negative(v):
    """
    Negate the input vector.

    Args:
        v: The input vector.

    Returns:
        The negated vector.
    """
    return np.negative(v)


def projected(v, other):
    """
    Project the vector onto another vector.

    Args:
        v: The vector to be projected.
        other: The vector onto which to project.

    Returns:
        The projected vector.
    """
    return multiply(normalized(other), dot_product(v, other) / vector_len(other))


def projected_left(v, other):
    """
    Calculate the projection of the vector on the left vector.

    Args:
        v: The vector.
        other: The left vector.

    Returns:
        The projected vector.
    """
    return minus(v, projected(v, other))


def reflect(v1, other: np.ndarray):
    """
    Reflect the vector.

    Args:
        v1: The vector.
        other: The other vector.

    Returns:
        The reflected vector.
    """
    v = normalized(other)
    return minus(v1, multiply(v, 2 * dot_product(v1, v)))


def some_perpendicular(v):
    """
    Find some perpendicular of the vector.

    Args:
        v: The input vector.

    Returns:
        The perpendicular vector.
    """
    return normalized(cross_product(v, np.add(v, 7)))
