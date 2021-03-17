---
title: "Testing randomness"
teaching: 15
exercises: 10
questions:
- "How can I test non-deterministic applications?"
objectives:
- "Be able to test functions that do not have an exact expected result for a given input."
keypoints:
- "By repeatedly calling the function being considered, tests can check that the expected statistical properties are observed."
---

Up until now we have been testing functions where the output is entirely
predictable. In these cases, a handful of tests is usually enough to provide
confidence that the software is working as expected. In the real world, however,
you might be developing a complex piece of sofware to implement an entirely new
algorithm, or model. In certain cases it might not even be clear what the
expected outcome is meant to be. Things can be particularly challenging when the
software is involves a stochastic element.

Let us consider a class to simulate the behaviour of a die. One is provided in
the dice package.

~~~
$ cd ../dice
~~~
{: .language-bash}

Let's import it and see how it works.

~~~
from dice import Die
help(Die)
~~~
{: .language-python}

How could we test that the die is fair?

Well, first of all we could check that the value of a die roll is in range.

~~~
def test_valid_roll():
    """ Test that a die roll is valid. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Roll the die.
    roll = die.roll()

    # Check that the value is valid.
    assert roll > 0 and roll < 7
~~~
{: .language-python}

~~~
$ pytest test/test_dice.py::test_valid_roll
~~~
{: .language-bash}

Great, that worked. But because die rolls are random, it could have been a fluke
that the test passed this time. In practice, we need to check that the
assertions hold repeatedly.

~~~
def test_always_valid_roll():
    """ Test that a die roll is "always" valid. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Roll the die lots of times.
    for i in range(10000):
        roll = die.roll()

        # Check that the value is valid.
        assert roll > 0 and roll < 7
~~~
{: .language-python}

~~~
$ pytest test/test_dice.py::test_always_valid_roll
~~~
{: .language-bash}

That is a better test. But does it guarantee that the die is fair? No, it only
guarantees that it won't return a number that isn't on the die.

![Comic reading: "int getRandomNumber() {return 4; // chosen by fair dice roll. guaranteed to be random. }"](https://imgs.xkcd.com/comics/random_number.png){:class="img-responsive"}

We still have more work to do to test that the die is fair.

Perhaps we should test the average value. We know that this should equal the sum
of the faces of the die, divided by the number of sides. For a six-sided die,
this is 3.5. Now, we will never achieve this exactly without an infinite number
of rolls (even getting within machine precision could take billions of rolls),
which we don't have time for.

Fortunately, `pytest` gives us a way to check things are approximately equal,
given some tolerance. `pytest.approx()` creates a number with an effective
"error bar"&mdash;a quantification of how far from the number we allow to be
considered "equal". Then any equality comparison with this approximate number
takes into account the uncertainty in it.

~~~
def test_average():
    """ Test that the average die roll is correct. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Work out the expected average roll.
    expect = sum(range(1, 7)) / 6

    # Calculate the sum of the die rolls.
    total = 0
    
    # Set the number of rolls.
    rolls = 100000

    for i in range(0, rolls):
        total += die.roll()

    # Check that the average matches the expected value.
    average = total / rolls
    assert average == pytest.approx(3.5, rel=1e-2)
~~~
{: .language-python}

~~~
$ pytest test/test_dice.py::test_average
~~~
{: .language-bash}

This takes us closer, but we're still not there. If we constructed a die with no
`2` or `5`, then the average roll would be `(1 + 3 + 4 + 6) / 4`; that is, 3.5.

We need to test that the _distribution_ of outcomes is correct, i.e. that each
of the six possible outcomes is equally likely.

~~~
def test_fair():
    """ Test that a die is fair. """

    # Intialise a standard, six-sided die.
    die = Die()

    # Set the number of rolls.
    rolls = 1000000

    # Create a dictionary to hold the tally for each outcome.
    tally = {}
    for i in range(1, 7):
        tally[i] = 0

    # Roll the die 'rolls' times.
    for i in range(0, rolls):
        tally[die.roll()] += 1

    # Assert that the probability is correct.
    for i in range(1, 7):
        assert tally[i] / rolls == pytest.approx(1 / 6, 1e-2)
~~~
{: .language-python}

~~~
$ pytest test/test_dice.py::test_fair
~~~
{: .language-bash}

The `Die` class has passed every test we've thrown at it, so we can be confident
that it is relatively bug-free for the cases we've tested for. Of course, so far
we've only tested 6-sided dice&mdash;we have no guarantee that it works for
other numbers of sides, yet.

You can extend this approach to any programming problem where you don't know the
exact answer up front, including those that are random and those that are just
exploratory. Start by focusing on what you do know, and write tests for that. As
you understand more what the expected results are, you can expand the test
suite.

> ## Two six-sided dice
>
> The file `test/test_dice.py` in the `dice` directory contains an empty
> function, `test_double_roll()`, for checking that the distribution for the sum
> of two six-sided die rolls is correct. Fill in the body of this function and
> run `pytest` to verify that your test passes.
>
> To implement this test, you'll need to know that the probability of the sum of
> two rolls of an \\(n\\)-sided die having a value \\(x\\) is given by:
> \\[p(x) = \frac{n-|x-(n+1)|}{n^2}\\]
> for \\(x\\) between 2 and 2\\(n\\). This is implemented as a helper function
> `prob_double_roll(x, n)` - for example, `prob_double_roll(4, 6)` calculates
> the probability of two 6-sided die rolls summing to 4.
>
> ~~~
> def prob_double_roll(x, n):
>     """
>     Expected probabilities for the sum of two dice.
>     """
>     # For two n-sided dice, the probability of two rolls summing to x is
>     # (n − |x−(n+1)|) / n^2, for x = 2 to 2n.
> 
>     return (n - abs(x - (n+1))) / n**2
> ~~~
> {: .language-python}
>
>> ## Solution
>>
>> ~~~
>> def test_double_roll():
>>     """ 
>>     Check that the probability for the sum of two n-sided dice matches
>>     the expected distribution.
>>     """
>> 
>>     # Store the expected probabilities for the sum of two dice.
>>     expect = {}
>>     for x in range(2, 13):
>>         expect[x] = prob_double_roll(x, sides)
>> 
>>     # Create a dictionary to hold the tally for each outcome.
>>     tally = {}
>>     for key in expect:
>>         tally[key] = 0
>> 
>>     # Initialise the die.
>>     die = Die(sides)
>> 
>>     # Roll two dice 'rolls' times.
>>     for i in range(0, rolls):
>> 
>>         # Sum the value of the two dice rolls.
>>         roll_sum = die.roll() + die.roll()
>> 
>>         # Increment the tally for the outcome.
>>         tally[roll_sum] += 1
>> 
>>     # Compute the probabilities and check with expected values.
>>     for key in tally:
>> 
>>         average = tally[key] / rolls
>>         assert average == pytest.approx(expect[key], rel=1e-2)
>> ~~~
>> {: .language-python}
> {: .solution}
{: .challenge}

> ## Two \\(n\\)-sided dice
>
> Parametrize the test in the previous challenge so that it works for any pair
> of \\(n\\)-sided dice. Test this using five- and seven-sided dice.
>
>> ## Solution
>>
>> ~~~
>> @pytest.mark.parametrize("sides, rolls", [(5, 5000000), (7, 5000000)])
>> def test_double_roll(sides, rolls):
>>     """ 
>>     Check that the probability for the sum of two n-sided dice matches
>>     the expected distribution.
>>     """
>> 
>>     # Store the expected probabilities for the sum of two dice.
>>     expect = {}
>>     for x in range(2, 2 * sides + 1):
>>         expect[x] = prob_double_roll(x, sides)
>> 
>>     # Create a dictionary to hold the tally for each outcome.
>>     tally = {}
>>     for key in expect:
>>         tally[key] = 0
>> 
>>     # Initialise the die.
>>     die = Die(sides)
>> 
>>     # Roll two dice 'rolls' times.
>>     for i in range(0, rolls):
>> 
>>         # Sum the value of the two dice rolls.
>>         roll_sum = die.roll() + die.roll()
>> 
>>         # Increment the tally for the outcome.
>>         tally[roll_sum] += 1
>> 
>>     # Compute the probabilities and check with expected values.
>>     for key in tally:
>> 
>>         average = tally[key] / rolls
>>         assert average == pytest.approx(expect[key], rel=1e-2)
>> ~~~
>> {: .language-python}
> {: .solution}
{: .challenge}
