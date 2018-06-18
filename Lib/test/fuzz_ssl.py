# Fuzz Tests for ssl

import os, random, time, _ssl

rnd = random.SystemRandom()
def fint(): return rnd.randint(0,3)
def fstr(): return os.urandom(rnd.randint(0,20))

def test():
  for _ in range(9999):
     bio = _ssl.MemoryBIO()
     for _ in range(fint()):
       if fint():
         try: bio.write(fstr())
         except _ssl.SSLError: pass
       if fint(): bio.read()
       if fint(): bio.write_eof()
       bio.pending
       bio.eof
     
     

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
