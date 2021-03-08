---
title: "pytest features"
teaching: 15
exercises: 10
questions:
- "How can I avoid repetition when writing similar tests?"
- "How can I test cases that I expect to raise exceptions?"
- "How can I test that documentation is up to date?"
objectives:
- "Be able to use parametrized tests."
- "Be able to write tests to verify that exceptions are correctly raised."
- "Be able to write docstrings that can be tested."
keypoints:
- "Use the `@pytest.mark.parametrize` decorator to run the same test multiple times with different data."
- "Use `with pytest.raises:` to define a block that is expected to raise an exception. The test will fail if the exception is not raised."
- "Use `pytest --doctest-modules` to check the examples given in any docstrings, and ensure that the output given is correct."
---

In the previous episode, we used `pytest` as a test runner. That is to say, it we used the fact that it looks through the current directory (and subdirectories) to find anything that looks like a test, and runs it. This is already incredibly useful, but is only a small slice of what pytest can do. When imported as a module into your tests, pytest gives additional functionality that makes your tests much more powerful.


## Avoiding repetition

Having a single test for a function is already infinitely better than having none, but one test only gives you so much confidence. The real power of a test suite is being able to test your functions under lots of different conditions.

Lets add a second test to check a different set of inputs and outputs to the `add_arrays` function and check that it passes:

~~~
from arrays import add_arrays

def test_add_arrays1():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expect = [5, 7, 9]
    
    output = add_arrays(a, b)
    
    assert output == expect

def test_add_arrays2():
    a = [-1, -5, -3]
    b = [-4, -3, 0]
    expect = [-5, -8, -3]
    
    output = add_arrays(a, b)
    
    assert output == expect
~~~
{: .language-python}

When we run `pytest` we can optionally pass the `-v` flag which puts it in verbose mode. This will print out the tests being run, one per line which I find a more useful view most of the time:

~~~
$ pytest -v
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 2 items                                          

test_arrays.py::test_add_arrays1 PASSED              [ 50%]
test_arrays.py::test_add_arrays2 PASSED              [100%]

==================== 2 passed in 0.07s =====================
~~~
{: .output}

We see both tests being run and passing. This will work well but we've had to repeat ourselves almost entirely in each test function. The only difference between the two functions is the inputs and outputs under test. Usually in this case in a normal Python function you would take these things as arguments and we can do the same thing here.

The actual logic of the function is the following:

~~~
def test_add_arrays(a, b, expect):
    output = add_arrays(a, b)
    assert output == expect
~~~
{: .language-python}

We then just need a way of passing the data we want to check into this function. Since we're not explicitly calling this function ourselves, we need a way to tell pytest that it should pass in certain arguments. For this, pytest provides a feature called _parametrization_. We label our function with a _decoration_ which allows pytest to run it mutliple times with different data.

> ## What's a decorator?
>
> A decorator is a function that takes a function and gives it extra behavior. This is done by putting the name of the decorator after an `@` sign, before the function definition. We won't go into detail about decorators in this lesson, but more details on what they are and how you can write your own can be found in the lesson on [Object-oriented programming with Python][python-oop-novice].
{: .callout}

To use this feature we must import the pytest module and use the `pytest.mark.parametrize`` decorator like the following:

~~~
import pytest

from arrays import add_arrays

@pytest.mark.parametrize("a, b, expect", [
    ([1, 2, 3],    [4, 5, 6],   [5, 7, 9]),
    ([-1, -5, -3], [-4, -3, 0], [-5, -8, -3]),
])
def test_add_arrays(a, b, expect):
    output = add_arrays(a, b)
    
    assert output == expect
~~~
{: .language-python}

The parametrize decorator takes two arguments:

1. a string containing the names of the parameters you want to pass in ("a, b, expect")
2. a list containing the values of the arguments you want to pass in

In this case, the test will be run twice. Once with each of the following values:

1. `a = [1, 2, 3]`, `b = [4, 5, 6]`, `expect = [5, 7, 9]`
2. `a = [-1, -5, -3]`, `b = [-4, -3, 0]`, `expect = [-5, -8, -3]`

Running these tests in verbose mode:

~~~
$ pytest -v
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 2 items                                          

test_arrays.py::test_add_arrays[a0-b0-expect0] PASSED [ 50%]
test_arrays.py::test_add_arrays[a1-b1-expect1] PASSED [100%]

==================== 2 passed in 0.03s =====================
~~~
{: .output}

We see that both tests have the same name (`test_arrays.py::test_add_arrays`) but each parametrization is differentiated with some square brackets.

> ## More parameters
>
> Add some more parameters sets to the `test_add_arrays` function. Try to think about corner-cases that might make the function fail. It's your job as the tester to try to "break" the code.
>
>> ## Solution
>>
>> ~~~
>> import pytest
>> 
>> from arrays import add_arrays
>> 
>> @pytest.mark.parametrize("a, b, expect", [
>>     ([1, 2, 3], [4, 5, 6], [5, 7, 9]),
>>     ([-1, -5, -3], [-4, -3, 0], [-5, -8, -3]), # Test zeros
>>     ([41, 0, 3], [4, 76, 32], [45, 76, 35]), # Test larger numbers
>>     ([], [], []), # Test empty lists
>> ])
>> def test_add_arrays(a, b, expect):
>>     output = add_arrays(a, b)
>>
>>     assert output == expect
>> ~~~
>> {: .language-python}
> {: .solution}
{: .challenge}


## Failing correctly

The interface of a function is made up of the _parameters_ it expects and the values that it _returns_. If a user of a function knows these things then they are able to use it correctly. This is why we make sure to include this information in the docstring for all our functions.

The other thing that is part of the interface of a function is any exceptions that are _raised_ by it.

To add explicit error handling to our function we need to do two things:

1. Add in a conditional raise statement:
   ~~~
   if len(x) != len(y):
       raise ValueError("Both arrays must have the same length.")
   ~~~
   {: .language-python}
2. Document in the docstring the fact that the function may raise something:
   ~~~
   Raises:
       ValueError: If the length of the lists ``x`` and ``y`` are different.
   ~~~
   {: .language-python}

Let's add these to `arrays.py`:

~~~
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
    
    Raises:
        ValueError: If the length of the lists ``x`` and ``y`` are different.

    Examples:
        >>> add_arrays([1, 4, 5], [4, 3, 5])
        [5, 7, 10]
    """
    
    if len(x) != len(y):
        raise ValueError("Both arrays must have the same length.")
    
    z = []
    for x_, y_ in zip(x, y):
        z.append(x_ + y_)

    return z
~~~
{: .language-python}

We can then test that the function correctly raises the exception when passed appropriate data. Inside a pytest function we can require that a specific exception is raised by using [`pytest-raises`][pytest.raises] in a `with` block. `pytest.raises` takes as an argument the type of an exception and if the block ends without that exception having been rasied, will fail the test.

It may seem strange that we're testing&mdash;and _requiring_&mdash;that the function raises an error but it's important that if we've told our users that the code will produce a certain error in specific circumstances that it does indeed do as we promise.

In our code we add a new test called `test_add_arrays_error` which does the check we require:

~~~
import pytest

from arrays import add_arrays

@pytest.mark.parametrize("a, b, expect", [
    ([1, 2, 3],    [4, 5, 6],   [5, 7, 9]),
    ([-1, -5, -3], [-4, -3, 0], [-5, -8, -3]),
])
def test_add_arrays(a, b, expect):
    output = add_arrays(a, b)
    
    assert output == expect

def test_add_arrays_error():
    a = [1, 2, 3]
    b = [4, 5]
    with pytest.raises(ValueError):
        output = add_arrays(a, b)
~~~
{: .language-python}

~~~
$ pytest -v
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 3 items

test_arrays.py::test_add_arrays[a0-b0-expect0] PASSED [ 33%]
test_arrays.py::test_add_arrays[a1-b1-expect1] PASSED [ 66%]
test_arrays.py::test_add_arrays_error PASSED         [100%]

==================== 3 passed in 0.03s =====================
~~~
{: .output}

> ## Parametrize tests with errors
>
> Try and parametrize the `test_add_arrays_error()` test that we've just written.
>
>> ## Solution
>>
>> ~~~
>> @pytest.mark.parametrize("a, b, expected_error", [
>>     ([1, 2, 3], [4, 5], ValueError),
>>     ([1, 2], [4, 5, 6], ValueError),
>> ])
>> def test_add_arrays_error(a, b, expected_error):
>>     with pytest.raises(expected_error):
>>         output = add_arrays(a, b)
>> ~~~
>> {: .language-python}
> {: .solution}
{: .challenge}

> ## Fix the function
>
> Write some parametrized tests for the `divide_arrays()` function. Think carefully about what kind of input might:
>
> 1. cause a bad implementation of the function to not work correctly, or
> 2. cause a good implementation of the function to raise an exception.
>
> Use your tests to identify and fix the bug in `divide_arrays()`
>
>> ## Solution
>>
>> ~~~
>> @pytest.mark.parametrize("a, b, expect", [
>>     ([1, 4, 12], [1, 2, 6], [1, 2, 2]), # Test integers
>>     ([-1, -45, 128], [-1, 9, -32], [1, -5, -4]), # Test negative numbers
>>     ([6], [3], [2]), # Test single-element lists
>>     ([1, 2, 3], [4, 5, 6], [0.25, 0.4, 0.5]), # Test non-integers
>>     ([], [], []), # Test empty lists
>> ])
>> def test_divide_arrays(a, b, expect):
>>     output = divide_arrays(a, b)
>>
>>     assert output == expect
>>
>>
>> @pytest.mark.parametrize("a, b, expected_error", [
>>     ([1, 2, 3], [4, 5], ValueError),
>>     ([1, 2], [4, 5, 6], ValueError),
>>     ([1, 2, 3], [0, 1, 2], ZeroDivisionError),
>> ])
>> def test_divide_arrays_error(a, b, expected_error):
>>     with pytest.raises(expected_error):
>>         output = divide_arrays(a, b)
>> ~~~
>> {: .language-python}
>>
>> In this case, the implementation of `divide_arrays` does not correctly deal with pairs of numbers that do not divide exactly. This is because the implementation has accidentally used `//` instead of `/`. Replacing `//` with `/` in the implementation allows the test to pass.
> {: .solution}
{: .challenge}


## Doctests

You may have noticed that the functions in `arrays.py` have extensive docstrings, including examples of how to use the functions defined there, looking like:

~~~
Examples:
    >>> add_arrays([1, 4, 5], [4, 3, 5])
    [5, 7, 10]
~~~
{: .language-python}

Since this is valid Python code, we can ask pytest to run this code and check that the output we claimed would be returned is correct. If we pass `--doctest-modules` to the `pytest` command, it will search `.py` files for docstrings with example blocks and run them:

~~~
$ pytest -v --doctest-modules
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 4 items                                          

arrays.py::arrays.add_arrays PASSED                  [ 25%]
test_arrays.py::test_add_arrays[a0-b0-expect0] PASSED [ 50%]
test_arrays.py::test_add_arrays[a1-b1-expect1] PASSED [ 75%]
test_arrays.py::test_add_arrays_error PASSED         [100%]

==================== 4 passed in 0.18s =====================
~~~
{: .output}

We see here the `arrays.py::arrays.add_arrays` test which has passed. If you get a warning about deprecation then ignore it, this is from a third-party module which is leaking through.

Doctests are a really valuable thing to have in your test suite as they ensure that any examples that you are giving work as expected. It's not uncommon for the code to change and for the documentation to be left behind and being able to automatically check all your examples avoids this.

> ## Break a doctest
>
> Try breaking one of the doctests, either by changing the example or by changing the function implementation. Re-run `pytest` and see how the output changes.
{: .challenge}

## Running specific tests

As you increase the number of tests you will come across situations where you only want to run a particular test. To do this, you follow pass the name of the test, as printed by `pytest -v` as an argument to `pytest`. So, if we want to run all tests in `test_arrays.py` we do:

~~~
$ pytest -v test_arrays.py
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 3 items                                          

test_arrays.py::test_add_arrays[a0-b0-expect0] PASSED [ 33%]
test_arrays.py::test_add_arrays[a1-b1-expect1] PASSED [ 66%]
test_arrays.py::test_add_arrays_error PASSED         [100%]

==================== 3 passed in 0.01s =====================
~~~
{: .output}

Or, if we want to specifically run the `test_add_arrays` test:

~~~
$ pytest -v test_arrays.py::test_add_arrays
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 2 items                                          

test_arrays.py::test_add_arrays[a0-b0-expect0] PASSED [ 50%]
test_arrays.py::test_add_arrays[a1-b1-expect1] PASSED [100%]

==================== 2 passed in 0.01s =====================
~~~
{: .output}

Or, if we want to run one parameter set for that test specifically:

~~~
$ pytest -v "test_arrays.py::test_add_arrays[a0-b0-expect0]"
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 1 item                                           

test_arrays.py::test_add_arrays[a0-b0-expect0] PASSED [100%]

==================== 1 passed in 0.01s =====================
~~~
{: .output}

Take a look at the output of `pytest -h` for more options. For example, you can tell `pytest` to only run the tests that failed on the last run with `pytest --last-failed`.



[pytest-raises]: https://docs.pytest.org/en/latest/reference.html#pytest-raises
[python-oop-novice]: https://edbennett.github.io/python-oop-novice
