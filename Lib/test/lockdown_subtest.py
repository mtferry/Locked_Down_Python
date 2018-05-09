import lockdownlib, os, io, sys, zipimport

try:
  import winreg
  has_winreg = True
except ModuleNotFoundError:
  has_winreg = False

blocked_cmds = [
  'import sys',
  'from os import *',
  'from os import system',
  'zipimport.zipimporter("foo")',
  'open("foo.txt","r")',
  'io.open("foo.txt","r")',
  'os.listdir(".")'
]

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
  ('os.environ["foo"]', TypeError("'NoneType' object is not subscriptable"))
]

allowed_cmds = [
  'os.cpu_count()'
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
