# Fuzz Test for _sre

import os, re, _sre, time

# Returns an int between 0 and n (inclusive) where n < 256
# Does so without using the random module since random depends on the math module which can't be built if re or _sre aren't working
def randint(n):
  while True:
    r = ord(os.urandom(1))
    if r <= (256//(n+1)*(n+1)):
      return r%(n+1)

def nop(*args, **kwargs): return 1

def fstr(): return os.urandom(randint(10))

def fint(): return randint(20)

def flst():
  l = []
  for _ in range(randint(20)):
    l.append(fint())
  return l

def fdict():
  d = {}
  for k in flst():
    d[k] = fint()
  return d

def test():
  rx = []

  while len(rx) < 100:
    try:
      args = [fstr(), 4, flst(), fint(), fdict(), tuple(flst())]
      r = _sre.compile(*args)
      rx.append((r,args))
    except (RuntimeError):
      pass

  for r, args in rx:
    for _ in range(9999):
      try:
        r.findall(fstr())
        r.findall(fstr(), fint())
        r.findall(fstr(), fint(), fint())

        list(r.finditer(fstr()))
        list(r.finditer(fstr(), fint()))
        list(r.finditer(fstr(), fint(), fint()))

        r.split(fstr())
        
        try:
          r.sub(fstr(), fstr())
          r.sub(fstr(), fstr(), fint())
          r.subn(fstr(), fstr())
          r.subn(fstr(), fstr(), fint())
        except (re.error, KeyError, IndexError):
          pass
        
        s = r.scanner(fstr())
        s.match()
        s.search()
        s.pattern
      except (RuntimeError, SystemError):
        pass

  fullmatch_matches = []
  while len(fullmatch_matches) < 100:
    for r, rargs in rx:
      args = [fstr(), fint(), fint()]
      try:
        m = r.fullmatch(*args)
        if m: fullmatch_matches.append((m, (args, rargs)))
      except RuntimeError:
        pass

  match_matches = []
  while len(match_matches) < 100:
    for r, rargs in rx:
      args = [fstr(), fint(), fint()]
      try:
        m = r.match(*args)
        if m: match_matches.append((m, (args, rargs)))
      except RuntimeError:
        pass

  search_matches = []
  while len(search_matches) < 100:
    for r, rargs in rx:
      args = [fstr(), fint(), fint()]
      try:
        m = r.search(*args)
        if m: search_matches.append((m, (args, rargs)))
      except RuntimeError:
        pass

  for m, args in (fullmatch_matches + match_matches + search_matches):
    for _ in range(9999):
      try:
        m.start(randint(255)-128)
        m.end(randint(255)-128)
        m.span(randint(255)-128)
        m.group(*flst())
        m.groupdict()
        m.lastgroup
        m.lastindex
      except IndexError:
        pass

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
