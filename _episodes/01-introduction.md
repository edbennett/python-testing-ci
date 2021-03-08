---
title: "Automating tests"
teaching: 15
exercises: 10
questions:
- "Why is automating tests important?"
- "What tools are available to help me automate tests?"
- "How can I use these tools to automate simple tests?"
objectives:
- "Understand the benefits of automating tests."
- "Be aware of test frameworks and runners such as pytest for automating tests."
- "Be able to write tests that can be detected and run by pytest."
keypoints:
- "Automated tests allow a program's complete behaviour to be tested every time changes are made, revealing any problems the changes may have caused."
- "Test frameworks provide tools to make writing tests easier, and test runners will automatically search for tests, run them, and verify that they give the correct results. pytest is an example of both of these."
- "Write tests functions that use `assert`s to check that the results are as expected. Name the functions to start with `test`, and put them in files starting with `test_` or ending with `_test.py`. Run the tests automatically by calling `pytest`."
---

Testing is extremely important. Without testing, you cannot be sure that your code is doing what you think. Testing is an integral part of software development, and where possible should be done _while_ you are writing code, not after the code has been written.

Most programmers' first approach to testing is to manually check that the code does the right thing. This might include running your code over a particular input file and making sure that a correct-looking plot comes out at the end, or running it with a few known inputs and checking that the results are the same as were obtained on the previous try? This is a start, but has a number of limitations:

* If the changes you've made have an effect on an area of code not relied on by the check that you're currently using, then how do you know that that effect hasn't broken anything?
* How can you be sure that there's not a subtle bug that means that the output is incorrect in a way that isn't immediately obvious?
* If there is a problem, how will you be able to work out exactly which line of code it causing it?

In order to be confident that our code it giving a correct output, a test suite is useful which provides a set of known inputs and checks that the code matches a set of known, expected outputs. To make it easier to locate where a bug is occuring, it's a good idea to make each individual test run over as small an amount of code as possible so that if _that_ test fails, you know where to look for the problem. In Python this "small unit of code" is usually a function.

To begin, let's look at a Python function to add lists of numbers. This is in the `arrays` directory, in the `arrays.py` file.

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

    Examples:
        >>> add_arrays([1, 4, 5], [4, 3, 5])
        [5, 7, 10]
    """
    z = []
    for x_, y_ in zip(x, y):
        z.append(x_ + y_)

    return z
~~~
{: .language-python}

Since the name of the module we want to test is `arrays`, let's make a file called `test_arrays.py` which contains the following:

~~~
from arrays import add_arrays

def test_add_arrays():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expect = [5, 7, 9]
    
    output = add_arrays(a, b)
    
    if output == expect:
        print("OK")
    else:
        print("BROKEN")

test_add_arrays()
~~~
{: .language-python}

This script defines a function called `test_add_arrays` which defines some known inputs (`a` and `b`) and a known, matching output (`expect`). It passes them to the function `add_arrays` and compares the output to expected. It will either print `OK` or `BROKEN` depending on whether it's working or not. Finally, we explicitly call the test function.

When we run the script in the Terminal, we see it output `OK`:

~~~
$ python test_arrays.py
~~~
{: .language-bash}

~~~
OK
~~~
{: .output}


> ## Break a test
>
> Break the test by changing either `a`, `b` or `expect` and rerun the test script. Make sure that it prints `BROKEN` in this case. Change it back to a working state once you've done this.
{: .challenge}

## Asserting

The method used here works and runs the code correctly but it doesn't give very useful output. If we had five test functions in our file and three of them were failing we'd see something like:

~~~
OK
BROKEN
OK
BROKEN
BROKEN
~~~
{: .output}

We'd then have to cross-check back to our code to see which tests the `BROKEN`s referred to.

To be able to automatically relate the output of the failing test to the place where your test failed, you can use an `assert` statement.

An `assert` statement is followed by something which is either _truthy_ or _falsy_. A falsy expression is something which, when converted to a bool gives `False`. This includes empty lists, the number `0` and `None`; everything else is considered truthy. The full list is available in [the documentation][truthiness].

If it is truthy then nothing happens, but if it is falsy then an exception is raised:

~~~
assert 5 == 5
assert 5 == 6
~~~
{: .language-python}

~~~
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-6-05598cd61862> in <module>
----> 1 assert 5 == 6

AssertionError: 
~~~
{: .output}

We can now use this assert statement in place of the `if`/`else` block:

~~~
from arrays import add_arrays

def test_add_arrays():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expect = [5, 7, 9]
    
    output = add_arrays(a, b)
    
    assert output == expect

test_add_arrays()
~~~
{: .language-python}

Now when we run the test script we get nothing printed on success:

~~~
$ python test_arrays.py
~~~
{: .language-bash}

but on a failure we get an error printed like:

~~~
Traceback (most recent call last):
  File "test_arrays.py", line 13, in <module>
    test_add_arrays()
  File "test_arrays.py", line 11, in test_add_arrays
    assert output == expect
AssertionError
~~~
{: .output}

Which, like all exception messages gives us the location in the file at which the error occurred. This has the avantage that if we had many test functions being run it would tell us which one failed and on which line.

The downside of using an `assert` like this is that as soon as one test fails, the whole script will halt and you'll only be informed of that one test.

## pytest

There's a few things that we've been doing so far that could be improved. Firstly, for every test function that we write we then have to explicitly call it at the bottom of the test script like` test_add_arrays()`. This is error-prone as we might write a test function and forget to call it and then we would miss any errors it would catch.

Secondly, we want nice, useful output from our test functions. Something better than the nothing/exception that a plain `assert` gives us. It would be nice to get a green `PASSED` for the good tests and a red `FAILED` for the bad ones alongside the name of the test in question.

Finally, we want to make sure that all tests are run even if a test early in the process fails.

Luckily, there is tool called _pytest_ which can give us all of these things. It will work on our test script almost exactly as written with only one change needed.

Remove the call to `test_add_arrays()` on the last line of the file:

~~~
from arrays import add_arrays

def test_add_arrays():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expect = [5, 7, 9]
    
    output = add_arrays(a, b)
    
    assert output == expect
~~~
{: .language-python}

And in the Terminal, run `pytest`:

~~~
$ pytest
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 1 item                                           

test_arrays.py .                                     [100%]

==================== 1 passed in 0.02s =====================
~~~
{: .output}

Pytest will do two stages. First it will try to locate all the test functions that it can find and then it will run each of them in turn, reporting the results.

Here you can see that it's found that the file `test_arrays.py` contains a single test function. The green dot next to the name of the file signifies the passing test. It then prints a summary at the end saying "1 passed".

The way that pytest works is that it looks for files which are called `test_*.py` or `*_test.py` and look inside those for functions whose names begin with `test`. It will then run those functions one at a time, reporting the results of each in turn.

To see what it looks like when you have a failing test, let's deliberately break the test code by giving a wrong expected result:

~~~
from arrays import add_arrays

def test_add_arrays():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expect = [5, 7, 999]  # Changed this to break the test
    
    output = add_arrays(a, b)
    
    assert output == expect
~~~
{: .language-python}

When we run this test with `pytest` it should tell us that the test is indeed failing:

~~~
$ pytest
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: requests-mock-1.8.0
collected 1 item                                           

test_arrays.py F                                     [100%]

========================= FAILURES =========================
_____________________ test_add_arrays ______________________

    def test_add_arrays():
        a = [1, 2, 3]
        b = [4, 5, 6]
        expect = [5, 7, 999]  # Changed this to break the test
    
        output = add_arrays(a, b)
    
>       assert output == expect
E       assert [5, 7, 9] == [5, 7, 999]
E         At index 2 diff: 9 != 999
E         Use -v to get the full diff

test_arrays.py:11: AssertionError
================= short test summary info ==================
FAILED test_arrays.py::test_add_arrays - assert [5, 7, 9]...
==================== 1 failed in 0.10s =====================
~~~
{: .output}

The output from this is better than we saw with the plain `assert`. It's printing the full context of the contents of the test function with the line where the `assert` is failing being marked with a `>`. It then gives an expanded explanation of why the assert failed. Before we just got `AssertionError` but now it prints out the contents of `output` and `expect` and tells us that at index 2 of the list it's finding a `9` where we told it to expect a `999`.

Before continuing, make sure that you change the file back to its previous contents by changing that `999` back to a `9`.


> ## Test subtraction
>
> In the `arrays.py` file you can see another function defined, `subtract_arrays()`. Write a test that verifies that this function works as expected.
>
>> ## Solution
>>
>> ~~~
>> from arrays import subtract_arrays
>> 
>> def test_subtract_arrays():
>>     a = [1, 2, 3]
>>     b = [6, 2, 1]
>>     expect = [-5, 0, 2]
>>
>>     output = subtract_arrays(a, b)
>>
>>     assert output == expect
>> ~~~
>> {: .language-python}
> {: .solution}
{: .challenge}

> ## Test first
>
> In the `arrays.py` file you can see that the function `multiply_arrays()` is present, but its functionality hasn't been written.
>
> First, write a test that this function should pass. Check that the `multiply_arrays()` function fails this test.
>
> Now, write a `multiply_arrays()` function that lets this test pass.
>
> This is the first step towards a process called "test-driven development" (TDD). We won't discuss TDD in detail today, but it is a popular methodology in some parts of the software world.
>
>> ## Solution
>>
>> ~~~
>> from arrays import multiply_arrays
>>
>> def test_multiply_arrays():
>>     a = [1, 2, 3]
>>     b = [4, 5, 6]
>>     expect = [1, 10, 18]
>>
>>     output = multiply_arrays
>>
>>     assert output == expect
>> ~~~
>> {: .language-python}
>>
>> ~~~
>> def multiply_arrays(x, y):
>>     """
>>     This function multiplies each element of one of the two passed lists
>>     from the other.
>>
>>     Args:
>>         x (list): The first list to multiply
>>         y (list): The second list to multiple
>>
>>     Returns:
>>         list: the pairwise products of ``x`` and ``y``.
>>
>>     Examples:
>>         >>> multiply_arrays([1, 4, 5], [4, 3, 5])
>>         [4, 12, 25]
>>     """
>>     if len(x) != len(y):
>>         raise ValueError("Both arrays must have the same length.")
>>
>>     z = []
>>     for x_, y_ in zip(x, y):
>>         z.append(x_ - y_)
>>
>>     return z
>> ~~~
>> {: .language-python}
> {: .solution}
{: .challenge}

{% include links.md %}

[truthiness]: https://docs.python.org/3/library/stdtypes.html#truth-value-testing
