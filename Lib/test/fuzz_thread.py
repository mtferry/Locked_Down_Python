# Fuzz Tests for _thread, _weakref and _queue

import os, random, time, _thread, _weakref, _queue

rnd = random.SystemRandom()
def fbool(): return not rnd.randint(0,1)
def fitem(): return rnd.choice([None, fbool(), rnd.random(), os.urandom(rnd.randint(0,9))])
def ftup(): return tuple([fitem() for _ in range(rnd.randint(0,99))])
def fdict(): return {k:v for k,v in zip(map(str, ftup()),ftup())}
def ffunc(q, *a): 
  _thread.get_ident()
  _thread._count()
  _thread.stack_size()
  local = _thread._local()

  try:
    q.empty()
    q.qsize()
    ln = rnd.randint(0,99)
    for _ in range(ln):
      rnd.choice([q.put, q.put_nowait])(fitem())
    for _ in range(ln):
      if fbool(): q.get(fbool(), rnd.random())
      else: q.get_nowait()
  except ReferenceError:
    pass

  return list(os.urandom(rnd.randint(0,99)))

class fclass(object):
  def __init__(s):
    s.tup = ftup()
  
def test():
  assert(_weakref.ReferenceType is _weakref.ref)
  for _ in range(99):
    time.sleep(5) # Throttle to avoid a MemoryError

    try: _weakref._remove_dead_weakref(dct, 'obj')
    except NameError: pass
    
    obj = fclass()
    _weakref.getweakrefcount
    dct = {'obj': _weakref.ref(obj)}
    _weakref.getweakrefs(obj)
    _weakref.getweakrefs(dct['obj'])
    dct['prox'] = _weakref.proxy(ffunc, ffunc)
    dct['oprox'] = _weakref.proxy(obj, ffunc)

    q = _queue.SimpleQueue()

    lock = rnd.choice([_thread.allocate_lock, _thread.allocate])()
    def lock_thread(*a, **k):
      try: rnd.choice([lock.acquire_lock, lock.acquire])(blocking=fbool(), timeout=rnd.randint(-10,10))
      except ValueError: pass
      rnd.choice([lock.locked, lock.locked_lock])()
      ffunc(q)
      try: rnd.choice([lock.release_lock, lock.release])()
      except RuntimeError: pass
      try:
        with lock: ffunc(q)
      except RuntimeError:
        pass
      rnd.choice([lock.locked, lock.locked_lock])()
      l = _thread._set_sentinel()
      if fbool(): rnd.choice([_thread.exit_thread, _thread.exit])()

    rlock = _thread.RLock()
    def rlock_thread(*a, **k):
      rlock.acquire(fbool())
      ffunc(q)
      rlock._is_owned()
      if fbool(): 
        try: rlock._release_save()
        except RuntimeError: pass
      if fbool(): rlock._acquire_restore((rnd.randint(-9999,9999),rnd.randint(-9999,9999)))
      try: rlock.release()
      except RuntimeError: pass
      try:
        with rlock: ffunc(q)
      except RuntimeError:
        pass
      rlock._is_owned()
      if fbool(): rnd.choice([_thread.exit_thread, _thread.exit])()

    for _ in range(99):
      repr(lock)
      repr(rlock)

      try: rnd.choice([_thread.start_new, _thread.start_new_thread])(rnd.choice([lock_thread, rlock_thread]), (q,) + ftup(), fdict())
      except RuntimeError: pass

      try: _thread.stack_size(rnd.randint(-99999999,99999999))
      except (ValueError, OverflowError): pass

      ffunc(q)

      try: _thread.interrupt_main()
      except KeyboardInterrupt: pass

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
