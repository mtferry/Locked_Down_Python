import sys

def lockdown():
  for m in sys.modules.values():
    try: m._lockdown()
    except AttributeError: pass
    m.__file__ = None
    m.__cached__ = None
    try: m.__spec__.origin = None
    except AttributeError: pass
  for a in ['executable', 'base_exec_prefix', 'base_prefix', 'dllhandle', 'exec_prefix', 'prefix', 'path_importer_cache', 'path']:
    setattr(sys, a, None)
  sys.modules['os'].environ._data = None
  sys.modules['site'].ENABLE_USER_SITE = None
  for a in ['PREFIXES', 'USER_BASE', 'USER_SITE']:
    setattr(sys.modules['site'], a, '')
