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

But before we do so, let us quickly recap what we learnt today.

## The purpose of a test

When you write a test you do this to gain (and in the case of automated tests
maintain) confidence into the correctness of your code. But in detail your tests
can serve a variety of purposes. It can be useful to keep in mind what you could
use tests for during your coding, so we compiled a certainly non-exhaustive list
of test purposes here. The major ones were discussed in the lesson; some more
exotic ones should be seen as suggestions for you to try. A test can have more
than one of these purposes:

* test for features - The first and simplest test that is capable of verifying
  the correctness of any feature (in the broadest sense) of your code. This is
  the obvious purpose of a test and encountered everywhere in the lesson.
* test for confidence (in a narrow sense) - Additional tests of the same
  features that are redundant in that they repeat a test for features with
  qualitatively similar input just to double-check. This is also encountered in
  the lesson, e.g. in the solution of [More parameters][more_parameters] large
  numbers aren't really that different from other numbers unless you run into
  overflow errors (one could even argue that testing the negative numbers in
  [pytest features][pytest_features] is not qualitatively different and rather
  to double check). One should be aware of the difference between testing for
  confidence and necessary feature tests. The former is a convenience that
  comes at the cost of longer test runs and so it is not always desirable to
  test redundantly (although certainly better than missing an aspect).
* test for edge-/corner-cases - Test special input or conditions for which a
  general algorithm needs to be specialised (e.g., NaNs, infinities, overflows,
  empty input, etc.). We did a [whole episode][edge_cases] on this.
* test for failures - This is part of feature testing but important enough to
  mention explicitly: The conditions under which your code fails are part of
  your interface and need to be tested. The user (that probably includes
  yourself) might rely on a raised exception or returned default value in the
  case of failure. Make sure they can and think of all the cases that your
  current approach cannot handle. Any changes in these (even those for the
  better) are changes of the interface and should appear intentionally. This was
  discussed in [pytest features][pytest_features].
* fuzzy testing - This is broader than testing for failures; if you have
  unexperienced or even malicious users of your project, they might run your
  code with inputs or under conditions that do not make any sense at all and are
  almost impossible to predict. Fuzzy testing is a strategy where you let the
  computer run your code with random input (sometimes down to the bit level) and
  make sure that not even the most far-fetched input can break your code. There
  are libraries for that, so you don't have to set up all the boilerplate
  yourself.
* regression test - After you have found a bug, you can write a test reproducing
  the precise conditions under which the bug appeared. Once you fixed it, your
  test will work fine and if a later change risks introducing this bug again, you
  can rest assured that it will be immediately signalled by a failing test.
* test as a reminder - In most contemporary test frameworks, you can mark a test
  as an "expected failure". Such tests are run during your standard test runs
  but the test framework will complain if they don't fail. This can be a
  convenient way of marking a to-do or a known bug that you don't have time to
  fix at the moment. It will preserve your precise intention, e.g., the precise
  conditions of the bug in code form and it might be an important information if
  a bug disappeared unexpectedly. Maybe another code change had an effect you
  did not intend?
* test for fixing an external interface - You can even test code did not write
  yourself. If you rely on a particular library, you don't have control over the
  evolution of that library, so it can be a good idea to write a few test cases
  that just use the interface of that library as you do it in your code. If they
  ever change or deprecate something about that interface, you don't have to
  chase down a rabbit hole of function calls to get the bottom of that but
  instead have a (hopefully well-named) test that immediately signals where the
  problem lies.
* test for learning an external interface - When you start using a new library,
  you might play around with it for a while before using it in production just
  to learn how it's used. Why not preserve this in automated tests? You have the
  same effect as if you, e.g., wrote a script or used an interactive session but
  you can come back and have a look at it again later. Also, you immediately fix
  the external interface (see previous item).

This is list certainly not something you want to implement as a whole. Some of
the purposes might simply not apply (e.g. fuzzy testing if you don't have
external users) or might not be worth the extra effort (e.g. fixing an external
interface that is expected to be very stable). But you might find yourself in a
situation where some of these are appropriate tools for your problem and you
might want to come back from time to time and refresh your memory. That said,
let's dive into the final exercise.

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
