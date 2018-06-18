import sys

SAFE_MODULES = ['gc', 'operator', '_operator', '_md5', '_sha1', '_sha256', '_sha512', '_blake2', '_sha3', '_hashlib', 'keyword', 'copyreg', 'builtins', 'token', 'stat', '_stat', '_string', 'possix', 'nt', '_json', '_sre', 'sre_constants', 'sys', 'winreg', 'zipimport', '_imp', 'marshal', 'itertools', 'errno', 'atexit', 'math', '_compat_pickle', 'msvcrt', '_winapi', 'select', '_posixsubprocess', 'binascii', 'zlib', '_bz2', '_lzma', '_signal', '_socket', '_ssl']

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
