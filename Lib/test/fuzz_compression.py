# Fuzz Tests for zlib, _bz2 and _lzma

import os, random, time, struct, zlib, _bz2, _lzma

rnd = random.SystemRandom()
def flong(): return struct.unpack('i', os.urandom(4))[0]
def fstr(): return os.urandom(rnd.randint(0,50))
def fbool(): return not rnd.randint(0,1)

def test_zlib():
  zlib.adler32(fstr(), flong())

  try: zlib.compress(fstr(), level=rnd.randint(-2, 10))
  except zlib.error: pass
  
  zlib.crc32(fstr(), flong())
  
  try: zlib.decompress(fstr(), wbits=rnd.randint(-50,50), bufsize=rnd.randint(-1,10000))
  except (ValueError, zlib.error): pass

  while True:
    try:
      obj = zlib.compressobj(
              level=rnd.randint(-2,10),
              method=rnd.choice([-1,8]),
              wbits=rnd.randint(-16,32),
              memLevel=rnd.randint(-1,10),
              strategy=rnd.randint(-1,5),
              zdict=rnd.choice([b'', fstr()]))
      break
    except (ValueError):
      continue

  obj.compress(fstr())
  obj.copy()

  for _ in range(99):
    try: obj.flush(rnd.randint(-1,9))
    except zlib.error: pass

  try: obj.copy()
  except ValueError: pass

  while True:
    try:
      obj = zlib.decompressobj(
              wbits=rnd.randint(-16,32),
              zdict=rnd.choice([b'', fstr()]))
      break
    except (ValueError):
      continue

  try: obj.decompress(fstr(), max_length=rnd.randint(0,99))
  except zlib.error: pass

  obj.unused_data
  obj.unconsumed_tail
  obj.eof

  obj.copy()
  
  try: obj.flush(rnd.randint(1,99))
  except zlib.error: pass

  try: obj.copy()
  except ValueError: pass

def test_bz2():
  obj = _bz2.BZ2Compressor(rnd.randint(1,9))
  for _ in range(rnd.randint(0,9)): obj.compress(fstr())
  obj.flush()
  if rnd.randint(0,1):
    try: obj.compress(fstr())
    except ValueError: pass
  if rnd.randint(0,1):
    try: obj.flush()
    except ValueError: pass

  obj = _bz2.BZ2Decompressor()
  for _ in range(rnd.randint(0,9)):
    try: obj.decompress(fstr(), max_length=rnd.randint(-1,99))
    except OSError: pass
  

def test_lzma():
  _lzma.is_check_supported(flong())
  
  def ffilter():
    f = {'id': flong()}
    if rnd.randint(0,1): f[fstr()] = flong()
    return f
  
  try: _lzma._encode_filter_properties(ffilter())
  except (OverflowError, ValueError): pass
  
  try: _lzma._decode_filter_properties(flong(),fstr())
  except (OverflowError, _lzma.LZMAError): pass
  
  while True:
    try:
      obj = _lzma.LZMACompressor(
              format=rnd.randint(0,3),
              check=rnd.randint(-5,15),
              preset=rnd.randint(0,9),
              filters=rnd.choice([None, [ffilter() for _ in range(rnd.randint(1,5))]]))
      break
    except (ValueError, _lzma.LZMAError):
      continue
  for _ in range(rnd.randint(0,9)): obj.compress(fstr())
  obj.flush()
  if rnd.randint(0,1):
    try: obj.compress(fstr())
    except ValueError: pass
  if rnd.randint(0,1):
    try: obj.flush()
    except ValueError: pass

  while True:
    try:
      obj = _lzma.LZMADecompressor(
              format=rnd.randint(0,3),
              memlimit=rnd.randint(-1,999999),
              filters=rnd.choice([None, list(range(rnd.randint(0,9)))]))
      break
    except (OverflowError, ValueError):
      continue
  for _ in range(rnd.randint(0,9)):
    try: obj.decompress(fstr(), max_length=rnd.randint(-1,99))
    except _lzma.LZMAError: pass
  
def test():
  for _ in range(999):
    test_zlib()
    test_bz2()
    test_lzma()

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
