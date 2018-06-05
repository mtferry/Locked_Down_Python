# Fuzz Tests for _string

import os, random, time, _string

rnd = random.SystemRandom()
def fstr(): return str(os.urandom(rnd.randint(0,10)))

def test():
  for _ in range(9999):
     try: list(_string.formatter_field_name_split(fstr())[1])
     except ValueError: pass

     try: list(_string.formatter_parser(fstr()))
     except ValueError: pass
    
if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
