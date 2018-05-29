Locked Down Python
==================

Locked Down Python (LDP) is a modified version of CPython for sandboxing code. It enables Python to make a seccomp-like one-way transition into a secure state where it is isolated from system resources. LDP runs anywhere CPython does.

.. contents::


Enabling Lockdown
^^^^^^^^^^^^^^^^^

LDP introduces a new module, lockdownlib, which can be used to enable lockdown::

    import lockdownlib
    lockdownlib.lockdown()

Lockdown disables any function that enable reading or modifying the file system (including import), processes or the operating system. It also prevents code from accessing the memory addresses and paths of objects and modules. For a longer (though not comprehensive) list of functions affected by lockdown, see the lockdown `unit test <https://github.com/mtferry/Locked_Down_Python/blob/master/Lib/test/test_lockdown.py>`_ and `sub-test <https://github.com/mtferry/Locked_Down_Python/blob/master/Lib/test/lockdown_subtest.py>`_.


Modules
^^^^^^^

Lockdown can be safely used with the modules that are loaded by Python at startup. Other modules may be safe to use with lockdown but many (such as ctypes, subprocess & socket) are not and importing them before enabling lockdown will enable mallicious code to escape the sandbox. The following is the whitelist of modules that can safely be used with LDP:

  - os
  - sys

TODO: Finish writing README
