import lockdownlib, os, io, sys, zipimport

try:
  import winreg
  has_winreg = True
except ModuleNotFoundError:
  has_winreg = False

valid_fd = os.open(__file__, os.O_RDONLY)
valid_fd_2 = os.open(__file__, os.O_RDONLY)

valid_id = id(valid_fd)

lockdown_exception = RuntimeError('lockdown is enabled')

# Parameters are valid enough enough that they should cover code past what Argument Clinic generates such that a lockdown_exception will raise if lockdown is enabled for a given command but invalid enough that the commands will fail without altering anything on disk

# These commands must raise lockdown_exception
blocked_cmds = [
  'import sys',
  'from os import *',
  'from os import system',
  'sys.setrecursionlimit(9)',
  'sys.getrecursionlimit()',
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
  'os.dup2(valid_fd, valid_fd_2)',
  'os.open("foo.txt", 0o777)',
  'os.pipe()',
  'os.access("foo.txt", 0)',
  'os.chdir("..")',
  'os.chmod("", 0)',
  'os.getcwd()',
  'os.getcwdb()'
]

# Same as above but these may not exist on some platforms
blocked_cmds_may_not_exist = [
  'os.ctermid()',
  'os.fchdir(valid_fd)',
  'os.getegid()',
  'os.geteuid()',
  'os.getgid()',
  'os.getgrouplist("foo", 0)',
  'os.getgroups()',
  'os.getpgid(0)',
  'os.getpriority(0,0)',
  'os.getresuid()',
  'os.getresgid()',
  'os.getuid()',
  'os.initgroups("foo", 0)',
  'os.setegid(0)',
  'os.seteuid(0)',
  'os.setgid(0)',
  'os.setgroups([])',
  'os.setpgrp()',
  'os.setpgid(-1, -1)',
  'os.setpriority(-1, -1, -1)',
  'os.setregid(-1, -1)',
  'os.setresgid(-1, -1, -1)',
  'os.setresuid(-1, -1, -1)',
  'os.setreuid(-1, -1)',
  'os.getsid(0)',
  'os.setsid()',
  'os.setuid(-1)',
  'os.uname()',
  'os.unsetenv("foo")',
  'os.fchmod(valid_fd, -1)',
  'os.fchown(valid_fd, -1, -1)',
  'os.fdatasync(valid_fd)',
  'os.fpathconf(valid_fd, "")',
  'os.fpathconf(valid_fd, "")',
  'os.fstatvfs(valid_fd)',
  'os.get_blocking(valid_fd)',
  'os.lockf(valid_fd, -1, -1)',
  'os.openpty()',
  'os.pipe2(0)',
  'os.posix_fallocate(valid_fd, 0, 0)',
  'os.posix_fadvise(valid_fd, 0, 0, 0)',
  'os.pread(valid_fd, 0, 0)',
  'os.pwrite(valid_fd, "", 0)',
  'os.tcgetpgrp(valid_fd)',
  'os.tcsetpgrp(valid_fd, -1)',
  'os.ttyname(valid_fd)',
  'os.get_inheritable(valid_fd)',
  'os.set_inheritable(valid_fd, -1)',
  'os.get_handle_inheritable(-1)',
  'os.set_handle_inheritable(-1, -1)',
  'os.chflags("", 0)',
  'os.chown("", 0, 0)',
  'os.chroot("..")',
  'os.fchdir(valid_fd)',
  'os.lchflags("",0)',
  'os.lchmod("",0)',
  'os.lchown("",0,0)',
  'os.link("","")'
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

# These shouldn't raise lockdown_exception but should raise another exception
# Since this will ignore AttributeErrors, we don't need to check if the platform supports these
allowed_cmds_with_exceptions = [
  'os.environ["foo"]',
  'os.environb["foo"]',
  'os.getenv("foo")',
  'os.getenvb("foo")',
  'os.ftruncate(valid_fd, 9999999)',
  'os.write(valid_fd, "")',
  'os.writev(valid_fd, [])',
  'os.sendfile(valid_fd, valid_fd_2, 0, 0)',
  'os.fsync(valid_fd)'
]

# These commands should run without any exceptions
allowed_cmds_no_exception = [
  'os.cpu_count()',
  'os.strerror(0)',
  'os.supports_bytes_environ',
  'os.fstat(valid_fd)',
  'os.isatty(valid_fd)',
  'os.lseek(valid_fd,0,0)',
  'os.read(valid_fd, 1)',
  'os.close(valid_fd)',
  'os.closerange(-4, -1)'
]

# If these exist, they shouldn't raise any exceptions
allowed_cmds_no_exception_may_not_exist = [
  'os.set_blocking(valid_fd, os.SF_SYNC)',
  'os.readv(valid_fd, [])'
]

# Special case: this will raise an exception if we're in a subprocess but it should never be a lockdown_exception
try:
  os.get_terminal_size()
  allowed_cmds_no_exception.append('os.get_terminal_size()')
except:
  allowed_cmds_with_exceptions.append('os.get_terminal_size()')

for cmd in blocked_cmds_may_not_exist:
  if hasattr(sys.modules[cmd[:cmd.index('.')]], cmd[cmd.index('.')+1:cmd.index('(')]):
    blocked_cmds.append(cmd)
    
for cmd in allowed_cmds_no_exception_may_not_exist:
  if hasattr(sys.modules[cmd[:cmd.index('.')]], cmd[cmd.index('.')+1:cmd.index('(')]):
    allowed_cmds_no_exception.append(cmd)

def check(cmd, expected=None, unexpected=None):
  global passed
  try:
    exec(cmd)
    res = None
  except Exception as ex:
    res = ex
  
  if res is None:
    res = 'NO EXCEPTION'
  
  p = (expected is not None and repr(expected)==repr(res)) or (unexpected is not None and repr(unexpected)!=repr(res))
  passed += p
  print(('PASSED' if p else ' FAILED'), cmd, repr(res))


lockdownlib.lockdown()
passed = 0

for cmd in blocked_cmds:
  check(cmd, expected = lockdown_exception)

for cmd in allowed_cmds_with_exceptions:
  check(cmd, unexpected = lockdown_exception)

for cmd in allowed_cmds_no_exception:
  check(cmd, expected = 'NO EXCEPTION')

print('PASSED' if id(os) != valid_id else 'FAILED', "Check that id isn't using actual pointers")
  
print()
print(passed, 'of', len(blocked_cmds+allowed_cmds_with_exceptions+allowed_cmds_no_exception), 'tests passed')
