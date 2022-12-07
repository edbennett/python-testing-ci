---
title: "Input data for tests"
teaching: 15
exercises: 10
questions:
- "How can I avoid repetition when defining input data for tests?"
- "How can I re-use test data that take significant time to generate?"
objectives:
- "Be able to define fixtures and use them in tests."
- "Understand when to mark fixtures for re-use and be able to do so."
keypoints:
- "A _fixture_ is a piece of test data that can be passed to multiple tests."
- "Define a fixture by creating a function with the `@pytest.fixture` decorator that returns the desired data. Any test that takes an argument of the same name will receive the data in the fixture."
- "Set the `scope` parameter to the `@pytest.fixture` decorator to control if and where the fixture is re-used across multiple tests. For example. `scope=\"session\"` reuses the fixture for the complete run of tests."
---

As we saw in the last section, when using parametrization it's often useful to
split your test function into two logical parts:

1. The data to be tested
2. The code to do the test

This is because we had a situation where we had one test function and multiple
examples to test. The opposite situation also happens where we have multiple
test functions, all of which want the same input data.

The name that pytest uses for "data which are provided to test functions" is
_fixture_ since it _fixes_ a set of data against which to test.

We'll start with the example of the `add_arrays` function to explain the syntax
but soon we'll need to use a example which demonstates the benefits more.

To make things clearer, we'll trim down the test file back to the basics. Just
one test for `add_arrays`:

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

To create our fixture we define a function which is decorated with the
`pytest.fixture` decorator. Apart from that, all the function needs to do is
return the data we want to provide to our tests, in this case, the two input
lists:

~~~
import pytest

@pytest.fixture
def pair_of_lists():
    return [1, 2, 3], [4, 5, 6]
~~~
{: .language-python}

To make the test functions make use of the fixture, we use the name of the
fixture (`pair_of_lists`) as a parameter of the test function, similar to how we
did with parametrization:

~~~
def test_add_arrays(pair_of_lists):
    ...
~~~
{: .language-python}

The data are now available inside the function using that name and we can use it
however we wish:

~~~
def test_add_arrays(pair_of_lists):
    a, b = pair_of_lists
    ...
~~~
{: .language-python}

This isn't how functions and arguments usually work in Python. pytest is doing
something magic here and is matching up the names of things which it knows are
fixtures (due to the decorator) with the names of parameters to test functions,
automatically running the fixture and passing in the data.

Note that `pair_of_lists` here is not a test function. It does not contain any
asserts and will not explicitly appear in the `pytest` output.

Putting it all together, we end up with:

~~~
import pytest

from arrays import add_arrays

@pytest.fixture
def pair_of_lists():
    return [1, 2, 3], [4, 5, 6]

def test_add_arrays(pair_of_lists):
    a, b = pair_of_lists
    expect = [5, 7, 9]

    output = add_arrays(a, b)

    assert output == expect
~~~
{: .language-python}

When we run the test suite, pytest will automatically run the `pair_of_lists`
function for any test that has it as an input and pass in the result.

~~~
$ pytest -v test_arrays.py
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: attrib-0.1.3, requests-mock-1.8.0, cov-2.10.1
collected 1 item

test_arrays.py::test_add_arrays PASSED               [100%]

==================== 1 passed in 0.01s =====================
~~~
{: .output}


## Big fixtures

It might be hard to see the benefit of fixtures with this rather contrived
example in which there aren't repeated uses of the same input data. So lets take
a look at a more sensible one where using a fixture makes sense.

Let's move now to the `books` directory, and looks at the file `books.py`, which
contains the following:

~~~
def word_count(text, word=''):
    """
    Count the number of occurences of ``word`` in a string.
    If ``word`` is not set, count all words.

    Args:
        text (str): the text corpus to search through
        word (str): the word to count instances of

    Returns:
        int: the count of ``word`` in ``text``
    """
    if word:
        count = 0
        for text_word in text.split():
            if text_word == word:
                count += 1
        return count
    else:
        return len(text.split())
~~~
{: .language-python}

To test this function we want a corpus of text to test it on. For the purposes
of this example and to simulate a complex data input, we will download the
contents of a particularly long novel from Project Gutenberg. Our test function
uses [`urllib.request`][urllib-request] to download the text, converts it to a
string and passes that to the `word_count` function.

At first we will make a single check: that the word "hat" appears 33 times in
the book:

~~~
import urllib.request

from books import word_count

def test_word_counts():
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    book_text = urllib.request.urlopen(url).read().decode('utf-8')
    assert word_count(book_text, "hat") == 33
~~~
{: .language-python}

~~~
$ pytest -v test_books.py
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: attrib-0.1.3, requests-mock-1.8.0, cov-2.10.1
collected 1 item

test_books.py::test_word_counts PASSED               [100%]

==================== 1 passed in 2.77s =====================
~~~
{: .output}

The test has passed and it took about two seconds. This is because it takes some
time to download the file from the internet. For this example we _want_ it to
take some time as it helps demonstrate the point. In reality you will come
across test data inputs which take some time (more than a few milliseconds) to
create.

This creates a tension between wanting to have a large test suite which covers
your code from lots of different angles and being able to run it very quickly
and easily. An ideal test suite will run as quickly as possible as it will
encourage you to run it more often. It's a good idea to have at least a subset
of your tests which run through in some number of seconds rather than hours.

Two seconds is not bad for this test but if we want to test against multiple
examples, it could get slow. Let's parametrise the test to add in a bunch more
inputs:

~~~
import urllib.request

import pytest

from books import word_count

@pytest.mark.parametrize('word, count',  [
    ('hat', 33),
    ('freedom', 71),
    ('electricity', 1),
    ('testing', 3),
    ('Prince', 1499),
    ('internet', 0),
    ('Russia', 71),
    ('Pierre', 1260),
    (None, 566334),
])
def test_word_counts(word, count):
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    book_text = urllib.request.urlopen(url).read().decode('utf-8')
    assert word_count(book_text, word) == count
~~~
{: .language-python}

~~~
$ pytest -v test_books.py
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: attrib-0.1.3, requests-mock-1.8.0, cov-2.10.1
collected 9 items

test_books.py::test_word_counts[hat-33] PASSED       [ 11%]
test_books.py::test_word_counts[freedom-71] PASSED   [ 22%]
test_books.py::test_word_counts[electricity-1] PASSED [ 33%]
test_books.py::test_word_counts[testing-3] PASSED    [ 44%]
test_books.py::test_word_counts[Prince-1499] PASSED  [ 55%]
test_books.py::test_word_counts[internet-0] PASSED   [ 66%]
test_books.py::test_word_counts[Russia-71] PASSED    [ 77%]
test_books.py::test_word_counts[Pierre-1260] PASSED  [ 88%]
test_books.py::test_word_counts[None-566334] PASSED  [100%]

==================== 9 passed in 27.46s ====================
~~~
{: .output}

You see here that it took about nine times as long. This is because the file is
downloaded afresh for every test example where really, it only _needs_ to be
downloaded once.

Let's move the slow setup into a fixture and give that as a parameter of the
test function:

~~~
import urllib.request

import pytest

from books import word_count

@pytest.fixture()
def long_book():
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    book_text = urllib.request.urlopen(url).read().decode('utf-8')
    return book_text

@pytest.mark.parametrize('word, count',  [
    ('hat', 33),
    ('freedom', 71),
    ('electricity', 1),
    ('testing', 3),
    ('Prince', 1499),
    ('internet', 0),
    ('Russia', 71),
    ('Pierre', 1260),
    (None, 566334),
])
def test_word_counts(long_book, word, count):
    assert word_count(long_book, word) == count
~~~
{: .language-python}

~~~
$ pytest -v test_books.py
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: attrib-0.1.3, requests-mock-1.8.0, cov-2.10.1
collected 9 items

test_books.py::test_word_counts[hat-33] PASSED       [ 11%]
test_books.py::test_word_counts[freedom-71] PASSED   [ 22%]
test_books.py::test_word_counts[electricity-1] PASSED [ 33%]
test_books.py::test_word_counts[testing-3] PASSED    [ 44%]
test_books.py::test_word_counts[Prince-1499] PASSED  [ 55%]
test_books.py::test_word_counts[internet-0] PASSED   [ 66%]
test_books.py::test_word_counts[Russia-71] PASSED    [ 77%]
test_books.py::test_word_counts[Pierre-1260] PASSED  [ 88%]
test_books.py::test_word_counts[None-566334] PASSED  [100%]

==================== 9 passed in 30.57s ====================
~~~
{: .output}

Perhaps surprisingly, it is still taking very long time!

By default a fixture will run once for every test function that uses it. In our
case we only need it to run once for all the tests in the test session so we can
pass in the scope parameter to `pytest.fixture` and set it to `"session"`:

~~~
import urllib.request

import pytest

from books import word_count

@pytest.fixture(scope="session")
def long_book():
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    book_text = urllib.request.urlopen(url).read().decode('utf-8')
    return book_text

@pytest.mark.parametrize('word, count',  [
    ('hat', 33),
    ('freedom', 71),
    ('electricity', 1),
    ('testing', 3),
    ('Prince', 1499),
    ('internet', 0),
    ('Russia', 71),
    ('Pierre', 1260),
    (None, 566334),
])
def test_word_counts(long_book, word, count):
    assert word_count(long_book, word) == count
~~~
{: .language-python}

~~~
$ pytest -v test_books.py
~~~
{: .language-bash}

~~~
=================== test session starts ====================
platform linux -- Python 3.8.5, pytest-6.0.1, py-1.9.0, pluggy-0.13.1 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/matt/projects/courses/software_engineering_best_practices
plugins: attrib-0.1.3, requests-mock-1.8.0, cov-2.10.1
collected 9 items

test_books.py::test_word_counts[hat-33] PASSED       [ 11%]
test_books.py::test_word_counts[freedom-71] PASSED   [ 22%]
test_books.py::test_word_counts[electricity-1] PASSED [ 33%]
test_books.py::test_word_counts[testing-3] PASSED    [ 44%]
test_books.py::test_word_counts[Prince-1499] PASSED  [ 55%]
test_books.py::test_word_counts[internet-0] PASSED   [ 66%]
test_books.py::test_word_counts[Russia-71] PASSED    [ 77%]
test_books.py::test_word_counts[Pierre-1260] PASSED  [ 88%]
test_books.py::test_word_counts[None-566334] PASSED  [100%]

==================== 9 passed in 3.06s =====================
~~~
{: .output}

Now it only takes about as long as a single test did since the slow part is only
being done once.

> ## Double check
>
> Add some more parameters to the test and check that it doesn't take any longer to run
{: .challenge}

> ## A double-edged sword
>
> We've seen that the default behaviour of pytest is to not re-use fixtures
> between different tests. This is because sometimes this will change the
> behaviour of the tests, and pytest prioritises correctness of the tests over
> their performance.
>
> What sort of behavior would functions have that failed in this way?
>
>> ## Solution
>>
>> If a test (or a function called by the test) accepts a mutable argument, and
>> then mutates it, then any other tests depending on that fixture that run after
>> the badly-behaved test will receive different data than were originally
>> specified in the fixture. This means that the test is likely to fail.
>>
>> Fixtures should only be re-used within groups of tests that do not mutate
>> them.
> {: .solution}
{: .challenge}

[urllib-request]: https://docs.python.org/3/library/urllib.request.html
