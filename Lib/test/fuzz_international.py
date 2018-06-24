# Fuzz Tests for unicodedata, _locale, _codecs, _multibytecodec, _codecs_cn, _codecs_hk, _codecs_jp, _codecs_kr, _codecs_tw and _codecs_iso2022

import os, random, time, warnings, unicodedata, _locale, _codecs, _multibytecodec, _codecs_cn, _codecs_hk, _codecs_jp, _codecs_kr, _codecs_tw, _codecs_iso2022

rnd = random.SystemRandom()
def fstr(): return os.urandom(rnd.randint(0,100))
def fint(): return rnd.randint(-20,20)
def fbool(): return not rnd.randint(0,1)
def ffunc(): return lambda *a, **k: rnd.choice([fstr(), fint()])

import test.fuzzhelper as fh
def fh_dir_func(i):
  d = dir(i)
  if 'errors' in d and fh.bool():
    setattr(i, 'errors', fh.str)
  return d
  
def test():
  warnings.filterwarnings('ignore')
  ucd_map = {a:getattr(unicodedata.ucd_3_2_0, a) for a in dir(unicodedata.ucd_3_2_0)}
  for _ in range(9999):
    for a in {**unicodedata.__dict__, **ucd_map, **_locale.__dict__, **_codecs.__dict__}.values():
      a
      repr(a)

      try: a()
      except (TypeError, UnicodeDecodeError, ValueError): pass

      try: a(fstr())
      except (TypeError, UnicodeDecodeError, ValueError): pass

      try: a(str(fstr()))
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass

      try: a(fstr(), fstr())
      except (TypeError, UnicodeDecodeError, ValueError): pass

      try: a(fstr(), str(fstr()))
      except (TypeError, UnicodeDecodeError, ValueError, LookupError): pass

      try: a(str(fstr()), str(fstr()))
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass
      
      try: a(fint(), fstr())
      except (TypeError, UnicodeDecodeError, ValueError, OSError): pass
      
      try: a(fint(), str(fstr()), str(fstr()))
      except (TypeError, UnicodeDecodeError, ValueError, OSError): pass
    
      try: a(ffunc())
      except (TypeError, UnicodeDecodeError, ValueError, OSError): pass

      try: a(ffunc(), str(fstr()))
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass

      try: a(ffunc(), str(fstr()), str(fstr()))
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass
      
      try: a(ffunc(), str(fstr()), fbool())
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass
      
      try: a(ffunc(), str(fstr()), fint(), fbool())
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass
      
      try: a(str(fstr()), ffunc())
      except (TypeError, UnicodeDecodeError, ValueError, LookupError, AttributeError): pass
      
    common_inputs = [
                     ((),{}),
                     ((fh.str,),{}),
                     ((fh.bytes,),{}),
                     ((fh.int,),{}),
                     ((fh.file_object,),{}),
                     ((fh.list,),{}),
                     ((fh.str,fh.str),{}),
                     ((fh.str,fh.bool),{}),
                    ]

    common_exceptions = (TypeError, ValueError, AttributeError, LookupError)

    fh.check(_multibytecodec, valid_inputs = common_inputs, expected_exceptions = common_exceptions, dir_func = fh_dir_func)
    fh.check(_codecs_cn, valid_inputs = common_inputs, expected_exceptions = common_exceptions)
    fh.check(_codecs_hk, valid_inputs = common_inputs, expected_exceptions = common_exceptions)
    fh.check(_codecs_jp, valid_inputs = common_inputs, expected_exceptions = common_exceptions)
    fh.check(_codecs_kr, valid_inputs = common_inputs, expected_exceptions = common_exceptions)
    fh.check(_codecs_tw, valid_inputs = common_inputs, expected_exceptions = common_exceptions)
    fh.check(_codecs_iso2022, valid_inputs = common_inputs, expected_exceptions = common_exceptions)

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
