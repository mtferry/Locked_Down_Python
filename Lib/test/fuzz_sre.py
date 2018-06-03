# _sre Fuzz Test

import os, random, re, _sre, time

rnd = random.SystemRandom()

def nop(*args, **kwargs): return 1

def fstr(): return os.urandom(rnd.randint(0,10))

def fint(): return rnd.randint(0,20)

def flst():
  l = []
  for _ in range(rnd.randint(0,20)):
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
        except re.error:
          pass
        
        s = r.scanner(fstr())
        s.match()
        s.search()
        s.pattern
      except RuntimeError:
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
        m.start(rnd.randint(-999,999))
        m.end(rnd.randint(-999,999))
        m.span(rnd.randint(-999,999))
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
