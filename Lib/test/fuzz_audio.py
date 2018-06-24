# Fuzz Test for audioop

import os, random, time, audioop

rnd = random.SystemRandom()
def fstr(): return os.urandom(rnd.randint(0,100))
def fint(): return rnd.randint(-20,20)

def test():
  for _ in range(9999):
    for a in audioop.__dict__.values():
      try: a(fstr(), fint())
      except (audioop.error, TypeError): pass
      
      try: a(fstr(), fstr())
      except (audioop.error, TypeError): pass
      
      try: a(fstr(), fstr(), fint())
      except (audioop.error, TypeError): pass

      try: a(fstr(), fint(), (fint(),fint()))
      except (audioop.error, TypeError, ValueError): pass
      
      try: a(fstr(), fint(), fint())
      except (audioop.error, TypeError): pass

      try: a(fstr(), fint(), fint(), fint())
      except (audioop.error, TypeError): pass

      try: a(fstr(), fint(), fint(), fint(), fint(), (fint(),fint()), fint(), fint())
      except (audioop.error, TypeError): pass


if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
