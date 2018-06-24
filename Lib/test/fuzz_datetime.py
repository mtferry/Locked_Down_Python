# Fuzz Tests for time and _datetime

import test.fuzzhelper as fh
import time, _datetime

def fh_date():
  return _datetime.datetime(fh.int(), fh.int(), fh.int())

def fh_tzinfo():
  class tz(_datetime.tzinfo):
    def utcoffset(*a):
      return _datetime.timedelta(minutes=fh.int)
  return tz()
  
def fh_time():
  return _datetime.time(fh.int(), fh.int(), fh.int(), fh.int(), fh_tzinfo())

def test():
  for _ in range(999):
    fh.check(time,
             valid_inputs = [
                            ((),{}),
                            ((fh.int,),{}),
                            ((fh.tuple,),{}),
                            ((fh.str, fh.tuple),{}),
                            ((fh.str,),{}),
                            ((fh.str, fh.str),{}),
                            ((fh_date, fh_time, fh_tzinfo),{}),
                            ],
             expected_exceptions = (TypeError, ValueError, OSError),
             dir_func = lambda i: set(dir(i))-{'sleep'})

    time.sleep(0)
    
    fh.check(_datetime,
             valid_inputs = [
                            ((),{}),
                            ((fh.int,),{}),
                            ((fh.int, fh.int),{}),
                            ((fh.str,),{}),
                            ((fh.str, fh.str),{}),
                            ((fh.int, fh.int, fh.int),{}),
                            ((fh.int, fh.int, fh.int, fh.int, fh_tzinfo),{}),
                            ((fh.int, fh.int, fh.int, fh.int, fh.int, fh.int),{}),
                            ((fh_date, fh_date),{}),
                            ((fh_date, fh_date, fh_tzinfo),{})
                            ],
             expected_exceptions = (TypeError, ValueError))

if __name__ == '__main__': fh.do_test_loop(test)
