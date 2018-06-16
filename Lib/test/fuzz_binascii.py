# Fuzz Tests for binascii

import os, random, time, struct, binascii

rnd = random.SystemRandom()
def flong(): return struct.unpack('i', os.urandom(4))[0]
def fstr(): return os.urandom(rnd.randint(0,50))
def fbool(): return not rnd.randint(0,1)

def test():
  for _ in range(9999):
    try: binascii.a2b_uu(fstr())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.b2a_uu(fstr())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.a2b_base64(fstr())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.b2a_base64(fstr(), newline=fbool())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.a2b_qp(fstr(), header=fbool())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.b2a_qp(fstr(), quotetabs=fbool(), istext=fbool(), header=fbool())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.a2b_hqx(fstr())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.rledecode_hqx(fstr())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.rlecode_hqx(fstr())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.b2a_hqx(fstr())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.crc_hqx(fstr(), flong())
    except (binascii.Error, binascii.Incomplete): pass
    
    try: binascii.crc32(fstr())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.crc32(fstr(), flong())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.b2a_hex(fstr())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.hexlify(fstr())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.a2b_hex(fstr())
    except (binascii.Error, binascii.Incomplete): pass

    try: binascii.unhexlify(fstr())
    except (binascii.Error, binascii.Incomplete): pass


if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
