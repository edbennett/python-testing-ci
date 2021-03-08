"""
This module provides a class for a fair, n-sided dice.

Author - Lester Hedges
"""

import random


class Die:
    """
    A simple class for an n-sided fair die.
    """

    def __init__(self, n=6, seed=None):
        """
        Construct an n-sided die.

        n -- The number of sides on the die.
        """

        if not type(n) is int:
            raise TypeError("The number of sides must be of type 'int'!")

        if n < 0:
            raise ValueError("The number of sides cannot be negative!")

        # Seed the random number generator.
        if seed is None:
            random.seed()
        else:
            random.seed(seed)

        # Set the number of sides.
        self._n = n

        # Initialise the value of the last die roll.
        self._last_roll = None

    def sides(self):
        """
        Return number of sides of the die.
        """
        return self._n

    def lastRoll(self):
        """
        Return the value of the last die roll.
        """
        return self._last_roll

    def roll(self):
        """
        Roll the die and return its value.
        """

        # Generate a random value between 1 and n inclusive.
        value = random.randint(1, self._n)

        # Store the value of the roll.
        self._last_roll = value

        # Return the value.
        return value
