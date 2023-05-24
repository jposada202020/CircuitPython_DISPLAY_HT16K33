Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-display-ht16k33/badge/?version=latest
    :target: https://circuitpython-display-ht16k33.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/pypi/v/circuitpython-display-ht16k33.svg
    :alt: latest version on PyPI
    :target: https://pypi.python.org/pypi/circuitpython-display-ht16k33

.. image:: https://static.pepy.tech/personalized-badge/circuitpython-display-ht16k33?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Pypi%20Downloads
    :alt: Total PyPI downloads
    :target: https://pepy.tech/project/circuitpython-display-ht16k33

.. image:: https://github.com/jposada202020/CircuitPython_DISPLAY-HT16K33/workflows/Build%20CI/badge.svg
    :target: https://github.com/jposada202020/CircuitPython_DISPLAY-HT16K33/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

On Display Simulation for an HT16K33 driver. Works with 16x8 and 8x8 matrices.

.. image:: https://github.com/jposada202020/CircuitPython_DISPLAY_HT16K33/blob/master/docs/7mwahe.gif

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Community Bundle library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-display_ht16k33/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-display_ht16k33

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-display_ht16k33

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-display_ht16k33

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install display_ht16k33

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

Take a look at the examples directory

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-display-ht16k33.readthedocs.io/>`_.
