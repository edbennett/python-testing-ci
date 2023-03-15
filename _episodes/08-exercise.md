---
title: "Putting it all together"
teaching: 5
exercises: 90
questions:
- "How can I apply all of these techniques at once to a real application?"
objectives:
- "Be able to apply testing and CI techniques to a piece of research software."
keypoints:
- "Testing and CI work well together to identify problems in research software and allow them to be fixed quickly."
- "If anything is unclear, or you get stuck, please ask for help!"
---

Now we have developed a range of skills relating to testing and continuous
integration, we can try putting them into practice on a real piece of research
software.

## The software

We are going to work with `pl_curves`, a piece of research software developed by
Dr Colin Sauzé at Aberystwyth University, which calculates Pareto–Lorenz (PL)
curves for calculating the relative abundance of different bacteria in a
community. It also calculates a Gini coefficient to show how evenly distributed
the different bacteria are. It already has tests written for most functions.

> ## Your task
> 
> 1. Fork [the repository][pl-curves]. You don't have push access to the original
>    repository, so you will need to use your own copy of it.
> 2. Enable GitHub actions on your fork,
>    as GitHub disables Actions for forks by default.
> 3. Update the CI and Codecov badges to point to your copy of the repository.
>    Pushing these changes should automatically run the test suite and update
>    the badges.
> 4. Create a virtual environment on your computer for the project, and install
>    the project's requirements, so you can run the test suite locally.
> 5. The current code is very outdated by now and you will see in a moment that
>    it does not work with a standard contemporary python installation anymore.
>    Assuming for a moment the tests would not exist, how would you feel about
>    the task of updating the code to run _correctly_ on a modern machine? Where
>    would you start? How confident would you feel that each and every line of
>    code works as intended?
> 6. Now we turn to the tests. Some of them fail currently. Work out why this is
>    happening, and fix the issues. Check that they are fixed in the CI workflow
>    as well.
> 7. Currently, the code is only tested for Python versions up to 3.6. Since
>    Python has moved on now, add 3.7, 3.8 and 3.9 as targets for the CI. Do the
>    tests pass now? If not, identify what has caused them to fail, and fix the
>    issues you identify. This is an important reason for having a test suite:
>    sometimes changes entirely external to your code will break your code.
>    Without a test suite, you don't know whether this has happened until
>    someone points out that your new results don't match your older ones!
>    Having CI set up allows easy testing of multiple different versions.
> 8. Currently the code is being tested against Ubuntu 18.04 (released April 2018).
>    A new long term support release of Ubuntu came out in April 2020 (version 20.04).
>    Upgrade the operating system being tested from Ubuntu 18.04 to Ubuntu 20.04.
>    As with upgrading Python, the test suite helps us check that the code still
>    runs on a newer operating system.
> 9. Upgrade to the most recent version of Pandas. Again, see if this breaks
>    anything. If it does, then fix the issues, and ensure that the test suite
>    passes again.
>
> Hint: In general, before changes are made to libraries that will break
> existing software using those libraries, they are "deprecated" for some period
> of time. During this time, the software will issue a warning of the impending
> breakage of the function, and give advice on how to modify your code so that
> a) the warning will go away, and b) the software will not break when the
> breaking change is made in a future version.
{: .challenge}


[pl-curves]: https://github.com/CDT-AIMLAC/pl_curves
