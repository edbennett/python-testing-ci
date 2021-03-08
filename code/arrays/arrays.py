"""
This module contains functions for manipulating and combining Python lists.
"""


def add_arrays(x, y):
    """
    This function adds together each element of the two passed lists.

    Args:
        x (list): The first list to add
        y (list): The second list to add

    Returns:
        list: the pairwise sums of ``x`` and ``y``.

    Examples:
        >>> add_arrays([1, 4, 5], [4, 3, 5])
        [5, 7, 10]
    """
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length.")

    z = []
    for x_, y_ in zip(x, y):
        z.append(x_ + y_)

    return z


def subtract_arrays(x, y):
    """
    This function subtracts each element of one of the two passed lists
    from the other.

    Args:
        x (list): The list to subtract from
        y (list): The list to subtract

    Returns:
        list: the pairwise differences of ``x`` and ``y``.

    Examples:
        >>> subtract_arrays([1, 4, 5], [4, 3, 5])
        [-3, 1, 0]
    """
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length.")

    z = []
    for x_, y_ in zip(x, y):
        z.append(x_ - y_)

    return z


def multiply_arrays(x, y):
    """TODO: Write this function."""

    pass


def divide_arrays(x, y):
    """
    This function divides each element of one of the two passed lists
    by the other.

    Args:
        x (list): The list to divide
        y (list): The list to divide by

    Returns:
        list: the pairwise quotient of ``x`` and ``y``.

    Examples:
        >>> divide_arrays([3, 12, -25], [3, -4, 5])
        [1, -3, -5]
    """

    if len(x) != len(y):
        raise ValueError("Both lists must have the same length.")

    z = []
    for x_, y_ in zip(x, y):
        z.append(x_ // y_)

    return z
