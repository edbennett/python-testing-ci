---
title: "Edge and corner cases, and integration testing"
teaching: 15
exercises: 10
questions:
- "What considerations are there when testing problems with boundaries?"
- "What are unit and integration tests?"
objectives:
- "Understand what edge and corner cases are, and how to test them."
- "Understand the difference between unit and integration tests, and the importance of both."
keypoints:
- "In problems that have fixed boundaries, an edge case is where a parameter sits on one of the boundaries."
- "In multidimensional problems with fixed boundaries, a corner case is where more than one parameter sits on one of the boundaries simultaneously."
- "Edge and corner cases need specific tests separate from the tests that apply across the whole problem."
- "Unit tests test the smallest units of functionality, usually functions."
- "Integration tests test that these units fit together correctly into larger programs."
---

So far we have been testing simple functions that take, at most, two parameters as arguments. There are no complex algorithms or logic at work, so the functions shouldn't behave differently depending on the input. The failure of these functions is down to oversights during programming, rather than anything fundamentally complicated in their workings.

In practice, this is often not the case. Functions might require many parameters and their execution and output can vary wildly depending on the input. In many cases there might be a normal range of parameter space where the function output is easy to predict, then other regions where the behaviour can be much more complex. When writing tests it is important that you cover as many cases as possible. You should push the boundaries of your software to make sure that it works as expected across the entire range of input under which it is meant to operate. This is known as having good _code coverage_, and will be discussed later.

Testing extreme values is often referred to as covering _edge_ and _corner_ cases. Typically, edge cases test situations where one parameter is at an extreme, while corner cases test two (or more in a multidimensional problems) edge cases simultaneously. However, sometimes the definition isn't so clear. (The principle of testing unusual input holds, though.)

In this section we will make use of the provided `grid` package.

~~~
$ cd ../grid
~~~
{: .language-bash}

This provides functionality for working with cells in a two-dimensional grid, like the 4&times;4 one shown below. (The values in each cell indicate the `(x, y)` position of the cell within the grid.)

| `(0, 3)` | `(1, 3)` | `(2, 3)` | `(3, 3)` |
| `(0, 2)` | `(1, 2)` | `(2, 2)` | `(3, 2)` |
| `(0, 1)` | `(1, 1)` | `(2, 1)` | `(3, 1)` |
| `(0, 0)` | `(1, 0)` | `(2, 0)` | `(3, 0)` |

Let's import the Cell class from the package and see how it works.

~~~
from grid import Cell
help(Cell)
~~~
{: .language-python}

We'll now create a Cell object that sits in the bulk of the grid and test that its neighbours are correct.

~~~
def test_bulk():
    """ Test that a cell in the bulk of the grid is correct. """

    # Instantiate a cell in the bulk of a 4x4 grid.
    c = Cell(2, 2, 4, 4)

    # Make sure that the cell has 4 neighbours.
    assert c.neighbours() == 4

    # Check the coordinates of the neighbours.
    assert c.left()  == (1, 2)
    assert c.right() == (3, 2)
    assert c.up()    == (2, 3)
    assert c.down()  == (2, 1)
~~~
{: .language-python}

Here we've instantiated a cell that sits at position `(2, 2)` in a 4&times;4 grid. Like Python, we choose to index from `0`.

Now let's check the neighbours of the cell. It should have 4 neighbours: `(1, 2)` to the left, `(3, 2)` to the right, `(2, 1)` below, and `(2, 3)` above.

Let's run the unit test with `pytest`.

~~~
$ pytest test/test_cell.py::test_bulk
~~~
{: .language-bash}

Great, everything worked as expected. Of course, the results are not unexpected, and we could have worked out the neighbours directly from the cell position by adding and subtracting 1 to the two indices.

Now let's check a cell on the left-hand edge of the grid at position `(0, 2)`. This should have 3 neighbours: one to the right, one below, and one above.

~~~
def test_left_edge():
    """ Test that a cell on the left edge of the grid is correct. """

    # Instantiate a cell on the left edge of a 4x4 grid.
    c = Cell(0, 2, 4, 4)

    # Make sure that the cell has 3 neighbours.
    assert c.neighbours() == 3

    # Check the coordinates of the neighbours.
    assert c.left()  == None
    assert c.right() == (1, 2)
    assert c.up()    == (0, 3)
    assert c.down()  == (0, 1)
~~~
{: .language-python}

~~~
$ pytest grid/test/test_cell.py::test_left_edge
~~~
{: .language-bash}

Fantastic, it works! The behaviour of the `Cell` object was fundamentally different because of the input (we triggered a different set of conditions). Had we done what we suggested above and assumed we could always add/subtract 1 from an index to go to the next cell, this test would have failed, as we would exceed the size of the grid.

Let's now check a cell at the bottom left-corner. This should only have two neigbours: one to the right, and one above.

~~~
def test_bottom_left_corner():
    """ Test that a cell on the bottom left corner of the grid is correct. """

    # Instantiate a cell at the bottom left corner of a 4x4 grid.
    c = Cell(0, 0, 4, 4)

    # Make sure that the cell has 2 neighbours.
    assert c.neighbours() == 2

    # Check the coordinates of the neighbours.
    assert c.left()  == None
    assert c.right() == (1, 0)
    assert c.up()    == (0, 1)
    assert c.down()  == None
~~~
{: .language-python}

~~~
$ pytest grid/test/test_cell.py::test_bottom_left_corner
~~~
{: .language-bash}

Once again a different condition has been triggered by our change of input. Here we have tested a corner case.

Corner cases are especially important to test, as it is very easy for two pieces of code we have written for dealing with different edges to conflict with one another. For example, triggering the right edge code could prevent the bottom edge code from executing. Explicitly testing corner cases guards against this kind of error.


## Integration tests

So far we have been testing functions and objects in isolation, so called _unit testing_. However, it is likely that you will write software with multiple objects that need to work together in order to do something useful. The process of checking that different pieces of code work together as intended is often called _integration testing_.

The `grid` module also contains a `Grid` class that generates a matrix of `Cell` objects and stores them internally. The user can then manipulate the cells by filling or emptying them. Let's import the class and see how it works.

~~~
grid = Grid(10, 10)
grid.fill(0, 0)
assert grid.nFilled() == 1
~~~
{: .language-python}

~~~
grid.fill(3, 7)
assert grid.nFilled() == 2
~~~
{: .language-python}

~~~
grid.empty(0, 0)
assert grid.nFilled() == 1
~~~
{: .language-python}

~~~
assert grid.cell(3, 7).occupied()
~~~
{: .language-python}

~~~
assert not grid.cell(0, 0).occupied()
~~~
{: .language-python}

> ## Class?
>
> `Grid` and `Cell` here are "classes", which you may not yet be familiar with. More detail on what these are, how they're used, and how you can build your own, can be found in the [Introduction to Object-Oriented Programming in Python lesson][python-oop-novice].
{: .callout}

> ## Bug hunting
>
> Run the complete set of unit tests for the `grid` directory.
>
> You will see a bug in `grid.py`. Fix this bug, and verify that the tests pass. Do the tests pass when the grid isn't square?
>
> For problems with nearest-neighbours, a good place to look would be where the checks are made in `_initializeNeighbours`.
{: .challenge}

> ## Test the `Grid`
>
> Create a new file `test/test_grid.py` to test the `Grid` class. You should test that the `fill` and `empty` functions behave as expected. The rules are that any cell in the grid can only be filled once.
>
> Fix any bugs that you find in this process, and verify that the fixes work and all tests pass.
{: .challenge}


[python-oop-novice]: https://edbennett.github.io/python-oop-novice
