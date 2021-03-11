---
title: Setup
---

## Python

If you do not already have a Python installation that you are happy with, then follow the instructions at [the Software Carpentry Python lesson][python-novice-inflammation] to get set up.


## pytest

Depending how you installed Python, you may already have pytest installed. To check this, open a terminal and run:

~~~
$ pytest --version
~~~
{: .language-bash}

This should output the version of pytest that you have installed; for example:

~~~
pytest 6.2.2
~~~
{: .output}

If instead you get an error, you will need to install pytest using pip:

~~~
$ pip install pytest
~~~
{: .language-bash}


## GitHub

To interact with continuous integration using GitHub Actions, you need to have a GitHub account. To do this, visit [GitHub][github] and sign up for an account, or check that you're able to log in.

## Download files

We'll be working with some existing pieces of example software for this lesson. Download [this archive][zip-file] and extract it to a convenient location&mdash;for example, your desktop.


{% include links.md %}

[github]: github.com
[python-novice-inflammation]: https://swcarpentry.github.io/python-novice-inflammation
[zip-file]: {{ page.root }}/files/code-testing.zip
