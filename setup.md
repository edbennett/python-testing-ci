---
title: Setup
---

## Python

If you do not already have a Python installation that you are happy with, then
follow the instructions in [the Software Carpentry workshop template
lesson][workshop-template-python] to get set up.


## pytest

Depending how you installed Python, you may already have pytest installed. To
check this, open a terminal and run:

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


## Git

To interact with continuous integration, you will need to be able to use the Git
version control system. If you don't already have Git installed, then follow the
instructions in [the Software Carpentry workshop template][workshop-template-git]
to get Git set up.


## GitHub

To interact with continuous integration using GitHub Actions, you need to have a
GitHub account. To do this, visit [GitHub][github] and sign up for an account,
or check that you're able to log in.

## Download files

We'll be working with some existing pieces of example software for this lesson.
Download [this archive][zip-file] and extract it to a convenient
location&mdash;for example, your desktop.


{% include links.md %}

[github]: github.com
[workshop-template-git]: https://carpentries.github.io/workshop-template/#git
[workshop-template-python]: https://carpentries.github.io/workshop-template/#python
[zip-file]: {{ page.root }}/files/code-testing.zip
