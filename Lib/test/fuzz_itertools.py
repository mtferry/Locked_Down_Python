# Fuzz Tests for itertools

import os, random, time, itertools

rnd = random.SystemRandom()
def fint(i=None): return rnd.randint(-9,9)
def fitem(): return rnd.choice([fint(), rnd.random(), os.urandom(abs(fint())), [], (), None])
def fiter(c=None):
  for _ in range(abs(fint())):
    yield fitem() if c is None else c()
def func(*args): return rnd.choice(args) if len(args) else fitem()

def do_iter_test(i):
  try: i.__reduce__()
  except (AttributeError, TypeError): pass
  try: i.__copy__()
  except AttributeError: pass
  try: i.__setstate__(tuple(fiter()))
  except (AttributeError, TypeError, ValueError): pass
  try: i.__sizeof__()
  except AttributeError: pass
  return list(i)

def test():
  for _ in range(999):
     try: do_iter_test(itertools.islice(itertools.count(fint(), fint()), fint()))
     except ValueError: pass
     
     try: do_iter_test(itertools.islice(itertools.cycle(fiter()), fint()))
     except ValueError: pass
     
     do_iter_test(itertools.repeat(fitem(), abs(fint())))
     
     try:do_iter_test(itertools.accumulate(fiter()))
     except TypeError: pass
     do_iter_test(itertools.accumulate(fiter(), func))

     do_iter_test(itertools.chain(fiter(fiter)))
     do_iter_test(itertools.chain(fiter(fiter)).from_iterable(fiter(fiter)))
     
     do_iter_test(itertools.compress(fiter(), fiter()))
     
     do_iter_test(itertools.dropwhile(fint, fiter()))
     do_iter_test(itertools.filterfalse(fint, fiter()))
     do_iter_test(do_iter_test(itertools.groupby(fiter(), fint)))
     
     try: do_iter_test(itertools.islice(fiter(), fint(), abs(fint()), abs(fint())))
     except ValueError: pass
     
     do_iter_test(itertools.starmap(func, fiter(fiter)))
     do_iter_test(itertools.takewhile(fint, fiter()))
     do_iter_test(do_iter_test(itertools.tee(fiter(), abs(fint()))))
     do_iter_test(itertools.zip_longest(fiter(fiter), fiter()))
     
     do_iter_test(itertools.product(fiter(), fiter()))
     do_iter_test(itertools.product(fiter(), repeat=rnd.randint(0,3)))
     do_iter_test(itertools.permutations(fiter(), func(abs(fint()),None)))
     do_iter_test(itertools.combinations(fiter(), abs(fint())))
     do_iter_test(itertools.combinations_with_replacement(fiter(), abs(fint())))
     
     do_iter_test(itertools._grouper(itertools.groupby(fiter(), fint), fiter()))
     do_iter_test(itertools._tee(fiter()))
     itertools._tee_dataobject(1, list(fiter()), None).__reduce__()

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
