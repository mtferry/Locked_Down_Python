# Fuzz Tests for _stat

import os, random, time, _stat

rnd = random.SystemRandom()
def fint(): return rnd.randint(-999999,999999)

def test():
  for _ in range(9999):
     for a in dir(_stat):
       f = getattr(_stat, a)
       if callable(f) and (a[0] == 'S' or a == 'filemode'):
         try: f(fint())
         except OverflowError: pass
    
if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
