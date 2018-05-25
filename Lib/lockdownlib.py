import sys

try: import nt as posix
except ImportError: import posix

def lockdown():
  posix._lockdown()
  for a in ['executable', 'base_exec_prefix', 'base_prefix', 'dllhandle', 'exec_prefix', 'prefix', 'path_importer_cache', 'path']:
    setattr(sys, a, None)
  sys.modules['os'].environ._data = None
  sys.modules['site'].ENABLE_USER_SITE = None
  for a in ['PREFIXES', 'USER_BASE', 'USER_SITE']:
    setattr(sys.modules['site'], a, '')
  for m in sys.modules:
    sys.modules[m].__file__ = None
    try: sys.modules[m].__spec__.origin = None
    except AttributeError: pass
