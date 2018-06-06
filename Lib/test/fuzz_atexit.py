# Fuzz Tests for atexit

import os, random, time, atexit

rnd = random.SystemRandom()
def fint(i=None): return rnd.randint(0,50)
def fargs(): 
  def f(*a, **k):
    return fint()
  a = [fint() for _ in range(fint())]
  k = {str(fint()):fint() for _ in range(fint())}
  return f, a, k

def test():
  for _ in range(999):
    args = [fargs() for _ in range(fint())]
     
    for f, a, k in args[fint():fint()]:
      atexit.register(f, *a, **k)

    if fint() == 0: atexit._clear()
    if fint() == 0: atexit._run_exitfuncs()

    for f, a, k in args[fint():fint()]:
      atexit.unregister(f)

    if fint() == 0: atexit._clear()
    if fint() == 0: atexit._run_exitfuncs()
    
    atexit._ncallbacks()

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
