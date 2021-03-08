def test_double_roll():
    pass


def prob_double_roll(x, n):
    """
    Expected probabilities for the sum of two dice.
    """
    # For two n-sided dice, the probability of two rolls summing to x is
    # (n − |x−(n+1)|) / n^2, for x = 2 to 2n.

    return (n - abs(x - (n + 1))) / n ** 2
