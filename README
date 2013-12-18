South 2
=======

This is the repository for South 2, the backport of Django's migrations
code into a separate installable package for Django 1.4, 1.5 and 1.6.

It requires Python 2.6 or newer.

**This code is incomplete and will not work. Do not use this yet.**


How it works
------------

Most of the code here is automatically pulled from the main Django
development tree and run through some light translation to get it to
import from south paths.

Then, a series of monkeypatches are applied to Django to give it just
enough of 1.7's features to get the code to run. This is a slightly
ridiculous way of doing things, but it saves porting over a lot of
code to only have minor changes, and means updates to migrations can
be pulled from Django directly and don't have to be written a
second time for South 2.

Why?
----

South 2 is not intended as a long term measure; it's just here so
that everyone can start using new-style migrations (including
third-party libraries shipping them) before they've upgraded to
1.7 or above.

It will be kept in sync with Django as long as possible, but will
not gain any major new features and may be slightly more unstable
than the native migration support in 1.7 and above. It's recommended
that, as a Django user, if you're running with South 2 you plan for
an eventual upgrade to Django 1.7 or above.
