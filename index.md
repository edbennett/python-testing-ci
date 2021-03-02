---
layout: lesson
root: .  # Is the only page that doesn't follow the pattern /:path/index.html
permalink: index.html  # Is the only page that doesn't follow the pattern /:path/index.html
---

Testing is a vital part of software development. Without it, we have no guarantee that the results that our software gives are correct, for any definition of "correct". While we all almost always do some checks when writing software that the bit we've just written does what we think it was going to, as our software grows in complexity then our work starts to have side-effects on other sections of the application which we may not think to re-test. Automating our testing allows us to verify all functionality in the application after every step of development, giving us an easier way of checking that everything is as we expect. In this lesson we will look at using [pytest][pytest] to test software written in Python, but tools for automated testing are available for most languages.

Continuous Integration (CI) takes automated testing to the next step, automatically running your tests whenever anyone commits and pushes a new revision of a piece of software to a repository. This means that even if you don't remember to run your tests yourself, you will still be made aware of any ways in which the software has stopped working as expected. In this lesson we will focus on the CI tools provided by [GitHub][github]; other services such as [GitLab][gitlab] also provide their own CI tools, as do other providers like [CircleCI][circleci].

> ## Prerequisites
>
> While automated testing tools are available in any language, this lesson relies on understanding the Python programming language. Continuous Integration requires working with a version control system, and in this lesson we will focus on Git. We will also make use of the Unix Shell to run the Python examples and interact with Git. If any of these concepts are unfamiliar, then we would recommend reviewing the Software Carpentry lessons for [Python][python-novice-inflammation], [Git][git-novice], and [the Unix Shell][shell-novice], respectively.
{: .prereq}

{% include links.md %}
circleci: https://circleci.com
git-novice: https://swcarpentry.github.io/git-novice
github: https://github.com
gitlab: https://gitlab.com
pytest: https://pytest.org
python-novice-inflammation: https://swcarpentry.github.io/python-novice-inflammation
shell-novice: https://swcarpentry.github.io/shell-novice
