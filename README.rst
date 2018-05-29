Locked Down Python
==================

Locked Down Python (LDP) is a modified version of CPython for sandboxing code. It enables Python to make a seccomp-like one-way transition into a secure state where it is isolated from system resources. LDP runs anywhere CPython does.

LDP introduces a new module, lockdownlib, which can be used to enable lockdown::

    import lockdownlib
    lockdownlib.lockdown()

Lockdown disables any function that enable reading or modifying the file system (including import), processes or the operating system. It also prevents code from accessing the memory addresses and paths of objects and modules. For a longer (though not comprehensive) list of functions affected by lockdown, see the
