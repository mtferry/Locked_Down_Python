import lockdownlib, os, io, sys, zipimport

try:
  import winreg
  has_winreg = True
except ModuleNotFoundError:
  has_winreg = False

valid_fd = os.open(__file__, os.O_RDONLY)
valid_fd_2 = os.open(__file__, os.O_RDONLY)
  
blocked_cmds = [
  'import sys',
  'from os import *',
  'from os import system',
  'zipimport.zipimporter("foo")',
  'open("foo.txt","r")',
  'io.open("foo.txt","r")',
  'os.listdir(".")',
  'os.chdir("..")',
  'os.getcwd()',
  'os.fsencode("foo.txt")',
  'os.fsdecode("foo.txt")',
  'os.fspath("foo.txt")',
  'os.get_exec_path()',
  'os.getlogin()',
  'os.getpid()',
  'os.getppid()',
  'os.putenv("foo", "bar")',
  'os.umask(-1)',
  'os.fdopen(valid_fd)',
  'os.device_encoding(valid_fd)',
  'os.dup(valid_fd)',
  'os.dup2(valid_fd, valid_fd_2)'
]

if hasattr(os, 'ctermid'): blocked_cmds.append('os.ctermid()')
if hasattr(os, 'fchdir'): blocked_cmds.append('os.fchdir(valid_fd)')
if hasattr(os, 'getegid'): blocked_cmds.append('os.getegid()')
if hasattr(os, 'geteuid'): blocked_cmds.append('os.geteuid()')
if hasattr(os, 'getgid'): blocked_cmds.append('os.getgid()')
if hasattr(os, 'getgrouplist'): blocked_cmds.append('os.getgrouplist("foo", 0)')
if hasattr(os, 'getgroups'): blocked_cmds.append('os.getgroups()')
if hasattr(os, 'getpgid'): blocked_cmds.append('os.getpgid(0)')
if hasattr(os, 'getpriority'): blocked_cmds.append('os.getpriority(0,0)')
if hasattr(os, 'getresuid'): blocked_cmds.append('os.getresuid()')
if hasattr(os, 'getresgid'): blocked_cmds.append('os.getresgid()')
if hasattr(os, 'getuid'): blocked_cmds.append('os.getuid()')
if hasattr(os, 'initgroups'): blocked_cmds.append('os.initgroups("foo", 0)')
if hasattr(os, 'setegid'): blocked_cmds.append('os.setegid(0)')
if hasattr(os, 'seteuid'): blocked_cmds.append('os.seteuid(0)')
if hasattr(os, 'setgid'): blocked_cmds.append('os.setgid(0)')
if hasattr(os, 'setgroups'): blocked_cmds.append('os.setgroups([])')
if hasattr(os, 'setpgrp'): blocked_cmds.append('os.setpgrp()')
if hasattr(os, 'setpgid'): blocked_cmds.append('os.setpgid(-1, -1)')
if hasattr(os, 'setpriority'): blocked_cmds.append('os.setpriority(-1, -1, -1)')
if hasattr(os, 'setregid'): blocked_cmds.append('os.setregid(-1, -1)')
if hasattr(os, 'setresgid'): blocked_cmds.append('os.setresgid(-1, -1, -1)')
if hasattr(os, 'setresuid'): blocked_cmds.append('os.setresuid(-1, -1, -1)')
if hasattr(os, 'setreuid'): blocked_cmds.append('os.setreuid(-1, -1)')
if hasattr(os, 'getsid'): blocked_cmds.append('os.getsid(0)')
if hasattr(os, 'setsid'): blocked_cmds.append('os.setsid()')
if hasattr(os, 'setuid'): blocked_cmds.append('os.setuid(-1)')
if hasattr(os, 'uname'): blocked_cmds.append('os.uname()')
if hasattr(os, 'unsetenv'): blocked_cmds.append('os.unsetenv("foo")')

if has_winreg:
  blocked_cmds.extend([
    'winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)',
    'winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "foo")',
    'winreg.DeleteKey(winreg.HKEY_CURRENT_USER, "cbe01b20-46dc-47d7-be3e-34a1d3f17c34")',
    'winreg.DeleteValue(winreg.HKEY_CURRENT_USER, "cbe01b20-46dc-47d7-be3e-34a1d3f17c34")',
    'winreg.EnumKey(winreg.HKEY_CURRENT_USER, 0)',
    'winreg.EnumValue(winreg.HKEY_CURRENT_USER, 0)',
    'winreg.ExpandEnvironmentStrings("%windir%")',
    'winreg.FlushKey(winreg.HKEY_CURRENT_USER)',
    'winreg.LoadKey(winreg.HKEY_USERS, "foo", "bar")',
    'winreg.OpenKey(winreg.HKEY_CURRENT_USER, "foo")',
    'winreg.QueryInfoKey(winreg.HKEY_CURRENT_USER)',
    'winreg.QueryValue(winreg.HKEY_CURRENT_USER, "foo")',
    'winreg.QueryValueEx(winreg.HKEY_CURRENT_USER, "foo")',
    'winreg.SaveKey(winreg.HKEY_USERS, "foo")',
    'winreg.SetValue(winreg.HKEY_CURRENT_USER, "foo", 0, "bar")',
    'winreg.SetValueEx(winreg.HKEY_CURRENT_USER, "foo", 0, 0, "bar")',
    'winreg.DisableReflectionKey(winreg.HKEY_CURRENT_USER)',
    'winreg.EnableReflectionKey(winreg.HKEY_CURRENT_USER)',
    'winreg.QueryReflectionKey(winreg.HKEY_CURRENT_USER)'
  ])

blocked_attributes = [
  ('os.environ["foo"]', TypeError("'NoneType' object is not subscriptable")),
  ('os.getenv("foo")', TypeError("'NoneType' object is not subscriptable"))
]

if hasattr(os, 'environb'): blocked_attributes.append(('os.environb["foo"]', TypeError("'NoneType' object is not subscriptable")))
if hasattr(os, 'getenvb'): blocked_attributes.append(('os.getenvb("foo")', TypeError("'NoneType' object is not subscriptable")))

allowed_cmds = [
  'os.cpu_count()',
  'os.strerror(0)',
  'os.supports_bytes_environ',
  'os.close(valid_fd)',
  'os.closerange(99999999, 99999999+3)'
]

def check(cmd, expected):
  global passed
  try:
    exec(cmd)
    res = None
  except Exception as ex:
    res = ex
  
  if res is None:
    res = 'NO EXCEPTION'
  
  p = (repr(expected)==repr(res))
  passed += p
  print(('PASSED' if p else 'FAILED'), cmd, repr(res))


lockdownlib.lockdown()
lockdown_exception = RuntimeError('lockdown is enabled')
passed = 0

for cmd in blocked_cmds:
  check(cmd, lockdown_exception)

for cmd, expected_exception in blocked_attributes:
  check(cmd, expected_exception)

for cmd in allowed_cmds:
  check(cmd, 'NO EXCEPTION')

print()
print(passed, 'of', len(blocked_cmds+blocked_attributes+allowed_cmds), 'tests passed')
