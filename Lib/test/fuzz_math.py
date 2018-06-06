# Fuzz Tests for math

import os, random, time, struct, math

rnd = random.SystemRandom()
def flong(): return struct.unpack('i', os.urandom(4))[0]
def fdouble(): return struct.unpack('d', os.urandom(8))[0]
def flist(u=3): return [rnd.choice([flong(),fdouble()]) for _ in range(rnd.randint(0,u))]

def test():
  for _ in range(999):
    for a in dir(math):
      f = getattr(math, a)
      if callable(f):
        args = flist()
        if len(args) > 0 and a == 'factorial' and args[0] > 99999:
          continue
        try: f(*args)
        except (ValueError, TypeError, OverflowError): pass
      else:
        f

    try: math.fsum(flist(999))
    except OverflowError: pass

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
