Locked Down Python
==================

Locked Down Python (LDP) is a modified version of CPython for sandboxing code. It enables Python to make a seccomp-like one-way transition into a secure state where it is isolated from system resources. LDP runs anywhere CPython does.

.. contents::

Building
^^^^^^^^
The build process for LDP is the same as CPython. See the `CPython Build Instructions <https://github.com/python/cpython/blob/ee994d7443a7e2809a5d49bd3679fc9c451a411b/README.rst#build-instructions>`_ for more information.


Enabling Lockdown
^^^^^^^^^^^^^^^^^

LDP introduces a new module, lockdownlib, which can be used to enable lockdown::

    import lockdownlib
    lockdownlib.lockdown()

Lockdown disables any functions that enable reading or modifying the file system (including import), processes or the operating system. It also prevents code from accessing the memory addresses and paths of objects and modules. Lockdown is not an atomic operation and any threads that may potentially execute unsafe code should wait until after lockdown completes before doing so. For a longer (though not comprehensive) list of functions affected by lockdown, see the lockdown `unit test <https://github.com/mtferry/Locked_Down_Python/blob/master/Lib/test/test_lockdown.py>`_ and `sub-test <https://github.com/mtferry/Locked_Down_Python/blob/master/Lib/test/lockdown_subtest.py>`_.


Modules
^^^^^^^

A list of modules that can be safely used with lockdown can be seen via::

  import lockdownlib
  lockdownlib.SAFE_MODULES

Any of the modules from the list can be used without compromissing the sandbox. Unsafe functions will be disabled when lockdown is enabled, however, it is still possible to access objects created before lockdown was enabled. For example, sockets created before lockdown can still accept connections and the output from subprocesses created before lockdown can still be read but new sockets can not be created, sockets can not be rebound and new subprocesses can't be run. Pure-Python modules can also be used though it is important to ensure that they do not cache anything that should not be accessable by unsafe code. Other modules may be safe to use with lockdown but many (such as ctypes) are not and importing them before enabling lockdown will enable mallicious code to escape the sandbox.

After enabling lockdown, a set of imported unsafe modules can be returned via::

  import sys, lockdownlib
  set(sys.modules)-set(lockdownlib.SAFE_MODULES)

If no unsafe modules are imported, the result should be an empty set. Note that a malicious module could remove itself from sys.modules so, while this is a useful technique for debugging, it is not foolproof. The only way to verify the safety of a module is by checking its source. However, even seemingly safe modules, particularly C modules, can be unsafe if their underlying code enables unsafe behavior (such as buffer overflows) due insecure code.

Demo
^^^^

You can try a demo of LDP `here <https://pacific-meadow-32681.herokuapp.com>`_.

License
^^^^^^^

As with CPython, LDP is liscensed under the PSFL. See the file "LICENSE" for information on the history of this software, terms & conditions for usage, and a DISCLAIMER OF ALL WARRANTIES. See `here <https://github.com/python/cpython#copyright-and-license-information>`_ for copyright information.

