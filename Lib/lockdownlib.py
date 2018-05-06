import sys

_lockdown = lockdown

def lockdown():
  _lockdown()
  sys.modules['os'].environ._data = None
  sys.executable = None
  for m in sys.modules:
    sys.modules[m].__file__ = None
    try: sys.modules[m].__spec__.origin = None
    except AttributeError: pass
