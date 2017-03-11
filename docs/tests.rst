..
    This file is part of INSPIRE.
    Copyright (C) 2015, 2016, 2017 CERN.

    INSPIRE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    INSPIRE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.

    In applying this licence, CERN does not waive the privileges and immunities
    granted to it by virtue of its status as an Intergovernmental Organization
    or submit itself to any jurisdiction.


Tests
=====


Inspire has several suites of tests, at the time of wrining this howto, it has
5 (that's mainly because it's the size of parallel runner pool in the free
tier on travis). But they mostly can be separated into 3 types:

* Unit tests: it's main goal is to test units of code (normaly functions),
  should be fast to run, and focus only on the code of the unit of code they
  are meant for, mocking if needed any external calls that are complex, slow
  or prone to failure. These tests should be relatively simple and stable.

* Integration tests: these focus on testing the interaction between the units
  of code that the unit tests handled, moking only external services. They are
  a bit slower than the unit tests, and a bit more complex and fragile.

* Acceptance tests: the acceptance tests will make sure that the end-to-end
  processes they test actually work ok. They are the slowest and the more
  complex of all, and as such, also the more britle, but give you a really high
  level of confidence that the business logic they test actually works.



Unit tests
----------

To run only the unit tests, you can just:

.. code-block:: console

    docker-compose -f docker-compose.tests.yml run --rm unit


Integration tests
-----------------
As stated before, the integration tests are actually split in several suites,
currently three:

* ``disambiguation``
* ``workflows``
* ``integration``

To run any of them, just use the same command as the unit tests changing the
name of the suite at the end, for example to run the ``integration`` suite:

.. code-block:: console

    docker-compose -f docker-compose.tests.yml run --rm integration


Acceptance tests
----------------

For the acceptance tests we use a framework called `Selenium`_, what it does is
actually fire up a browser (we use firefox) and click around, do requests and
assert about the contents of the page.

This framework can run on the background, or can show the browser window on
your laptop. So let's see how to run it:

Via Docker
~~~~~~~~~~

1. If you have not installed ``docker`` and ``docker-compose``, `install them now`_.

2. Run ``docker-compose``:

.. code-block:: bash

  $ docker-compose -f docker-compose.test.yml run --rm acceptance


Via Docker showing the Firefox window (Linux)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check the first step in the `Via Docker`_ section.

2. Add the root user to the list allowed by **X11**:

.. code-block:: bash

  $ xhost local:root
  non-network local connections being added to access control list

3. Run ``docker-compose``:

.. code-block:: bash

  $ docker-compose -f docker-compose.test.yml run --rm acceptance


Via Docker showing the Firefox window (MacOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check the first step in the `Via Docker`_ section.

2. Install **XQuartz**: go to the `XQuartz website`_ and install the latest
   version. For example, run:

.. code-block:: bash

  $ brew cask install xquartz

3. Having installed **XQuartz**, run it and open the **XQuartz** ->
   **Preferences** menu from the bar. Go to the last tab, **Security**, enable
   both the **"Authenticate connections"** and **"Allow connections from network
   clients"** checkboxes, then restart your computer.

.. figure:: images/xquartz_security.jpg
  :align: center
  :alt: XQuartz security options we recommend.
  :scale: 45%

4. Write down the IP address of your computer because you will need it later:

.. code-block:: bash

  $ ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'
  123.456.7.890

5. Add the IP address of your computer to the list allowed by **XQuartz**:

.. code-block:: bash

  $ xhost + 123.456.7.890
  123.456.7.890 being added to access control list

6. Set the ``$DISPLAY`` environment variable to the same IP address, followed by
   the id of your display (in this case, ``:0``):

.. code-block:: bash

  $ export DISPLAY=123.456.7.890:0

7. Run ``docker-compose``:

.. code-block:: bash

  $ docker-compose -f docker-compose.test.yml run --rm acceptance


How to Write the Selenium Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Selenium Test Framework
.......................

INSPIRE's Selenium tests are written using an in-house framework called BAT
(:file:`inspirehep/bat`). The framework is made of four main components:

- `Tests`
- `Pages`
- `Arsenic`
- `ArsenicResponse`

.. figure:: images/BAT_Framework.png


Test functions
..............

Tests don't call directly Selenium methods, but call methods on `Pages`, which
are eventually translated to Selenium calls.

Tests are intended to be imperative descriptions of what the user does and what
they expect to see. For example

.. code-block:: python

    def test_mail_format(login):
        create_author.go_to()
        assert create_author.write_mail('wrong mail').has_error()
        assert not create_author.write_mail('me@me.com').has_error()

asserts that, when the user visits the "Create Author" page and writes ``wrong
mail``, they see an error, while when they visit the same page but write a valid
email, they don't see it.


Pages
.....

Pages are abstractions of web pages served by INSPIRE. Concretely, a page is a
collection of methods in a module that implement the various action that a user
can take when interacting with that page. For example the

.. code-block:: python

    def go_to():
        Arsenic().get(os.environ['SERVER_NAME'] + '/authors/new')

method in ``inspirehep/bat/pages/create_author.py`` represents the action of
visiting the "Create Author" page, while

.. code-block:: python

    def write_institution(institution, expected_data):
        def _write_institution():
            return expected_data in Arsenic().write_in_autocomplete_field(
                'institution_history-0-name', institution)

        return ArsenicResponse(_write_institution)

in the same module represents the action of filling the autocomplete field
of id ``institution_history-0-name`` with the content of the ``institution``
variable.

Note that the latter method returns a closure over ``expected_data`` and
``institution`` which is going to be used by an ``has_error`` call to determine
if the action was successful or not.


Arsenic
.......

The ``Arsenic`` class is a proxy to the Selenium object, plus some
INSPIRE-specific methods added on top.


ArsenicResponse
...............

As mentioned above, an ``ArsenicResponse`` wraps a closure that is going to be
used by an ``has_error`` call to determine if the action executed
successfully.


.. _Selenium: http://docs.seleniumhq.org/
.. _install them now: https://github.com/inspirehep/inspire-next/pull/1015
.. _`XQuartz website`: https://www.xquartz.org/

