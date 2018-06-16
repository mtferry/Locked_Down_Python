# Runs all fuzz tests in a loop

import sys, time
_is_subprocess = __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'subprocess'

if not _is_subprocess:
  import os, test, subprocess
  
  tests = []
  for tpath in test.__path__:
    for test in os.listdir(tpath):
      if test.startswith('fuzz_') and test != os.path.basename(__file__):
        tests.append(getattr(__import__('test.'+test[:-3]), test[:-3]))
  
  if __name__ == '__main__':
    print('Start Time:', time.ctime())
    subprocess.Popen(sys.executable + ' -m test.fuzz_all subprocess')
    for i in range(1,99999):
      for t in tests:
        t.test()
        print('End of', t.__name__, 'for Iteration', i, '-', time.ctime())

if _is_subprocess:
  import random, struct, lockdownlib
  rnd = random.SystemRandom()
  safe_modules = []
  for m in lockdownlib.SAFE_MODULES:
    try: safe_modules.append(__import__(m))
    except ModuleNotFoundError: pass

  def fargs(depth=0):
    args = []
    for _ in range(rnd.randint(0, 8)):
      c = rnd.randint(1, 8 if depth<1 else 5)
      if c == 1: args.append(rnd.randint(-999999,999999))
      elif c == 2: args.append(os.urandom(rnd.randint(0,10)))
      elif c == 3: args.append(fargs)
      elif c == 4: args.append(struct.unpack('i', os.urandom(4))[0])
      elif c == 5: args.append(struct.unpack('d', os.urandom(8))[0])
      elif c == 6: args.append(fargs(depth+1))
      elif c == 7: args.append(tuple(fargs(depth+1)))
      elif c == 8: args.append({k:v for k, v in zip(fargs(), fargs())})
    return args

  if __name__ == '__main__':
    lockdownlib.lockdown()
    for i in range(1,99999):   
      for _ in range(999999):
        # m = rnd.choice(list(sys.modules.values()))   Someday. Not yet though.
        m = rnd.choice(safe_modules)
        a = getattr(m, rnd.choice(dir(m)))
        try:
          a(*fargs) if callable(a) else a
        except:
          pass
      print('Finished testing several random functions and attributes for Iteration', i, '-', time.ctime())
