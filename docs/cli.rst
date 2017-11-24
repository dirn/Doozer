======================
Command Line Interface
======================

Doozer provides the following command line interface.

.. autoprogram:: doozer.cli:parser
   :prog: doozer

Further Details
===============

When developing locally, applications often need to be restarted as changes are
made. To make this easier, Doozer provides a ``--reloader`` option to the
``run`` command. With this option enabled, Doozer will watch an application's
root directory and restart the application automatically when changes are
detected::

    $ python -m doozer run file_printer --reloader

.. note:: The ``--reloader`` option is not recommended for production use.

It's also possible to enable Doozer's :ref:`debug mode` through the ``--debug``
option::

    $ python -m doozer run file_printer --debug

.. note:: The ``--debug`` option is not recommended for production use.

This will also enable the reloader.

Extending the Command Line
==========================

For information about how to extension Doozer's command line interface, see
:ref:`extending-the-cli`.
