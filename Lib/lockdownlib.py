import sys

_lockdown = lockdown

def lockdown():
  _lockdown()
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

def unittest():
  import os, io
  lockdown()
  passed = 0
  blocked_cmds = [
      'import sys',
      'open("foo.txt","r")',
      'io.open("foo.txt","r")',
      'os.listdir(".")'
    ]
  allowed_cmds = [
      'os.cpu_count()'
    ]
  for cmd in blocked_cmds:
    try:
      exec(cmd)
      print("FAILED", cmd, "NO EXCEPTION RAISED")
    except Exception as ex:
      if type(ex) is RuntimeError and ex.args == ('lockdown is enabled',):
        passed += 1
        print('PASSED', cmd)
      else:
        print('FAILED', cmd, repr(ex))
  for cmd in allowed_cmds:
    try:
      exec(cmd)
      passed += 1
      print('PASSED', cmd)
    except Exception as ex:
      print('FAILED', cmd, repr(ex))
  print('\n', passed, 'of', len(blocked_cmds+allowed_cmds), 'tests passed')

if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == 'unittest':
    unittest()
