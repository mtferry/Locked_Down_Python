# Fuzz Tests for marshal

import os, random, time, marshal

rnd = random.SystemRandom()
def fint(): return rnd.randint(-1,9)
def fstr(): return os.urandom(rnd.randint(0,20))

def test():
  class FileLikeObject(object):
    def write(s): pass
    def read(s): return os.urandom(s) if fint() != 0 else b''
  for _ in range(9999):
     data = fstr()

     try: data = marshal.loads(data)
     except Exception: pass

     marshal.dump(data, FileLikeObject)
     marshal.dump(data, FileLikeObject, fint())
     marshal.dumps(data)
     marshal.dumps(data, fint())

     try: marshal.load(FileLikeObject)
     except Exception: pass

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
