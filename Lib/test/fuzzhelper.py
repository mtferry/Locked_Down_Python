import builtins, os, time, random

rand = random.SystemRandom()

def bool():
  return not rand.randint(0,1)

def int():
  return rand.randint(-99,99)

def bytes():
  return os.urandom(rand.randint(0,10))

def str():
  return builtins.str(bytes())

def object(depth_limit=1):
  possible = [None, bool(), rand.random(), str(), int(), klass()()]
  if depth_limit > 0: possible.append(list(depth_limit-1))
  return rand.choice(possible)

def list(depth_limit=1):
  return [object(depth_limit) for _ in range(rand.randint(0,9))]

def tuple():
  return builtins.tuple(list())

def dict():
  return {k:v for k,v in zip(map(builtins.str, tuple()),tuple())}

def function():
  def f(*a, **k):
    return object()
  return f

def klass():
  class k(): pass
  return k
  
def file_object():
  class fobj():
    def read(*a): return bytes()
    def write(*a): return None
  return fobj

def check(item, valid_inputs, expected_exceptions, depth_limit=2, dir_func=dir):
  if depth_limit < 1:
    return

  for a in dir_func(item):
    try:
      check(getattr(item, a), valid_inputs, expected_exceptions, depth_limit-1)
    except expected_exceptions:
      pass
    except Exception as ex:
      print('[Exception at Attribute]', item, a, ex)
      raise ex

  if callable(item):
    for iargs, ikwargs in valid_inputs:
      try:
        check(item(*[a() for a in iargs],**{k:v() for k,v in ikwargs.items()}), valid_inputs, expected_exceptions, depth_limit-1)
      except expected_exceptions:
        pass
      except Exception as ex:
        print('[Exception at Call]', item, iargs, ikwargs, ex)
        raise ex

def do_test_loop(test):
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
