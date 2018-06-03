# Fuzz Tests for _hashlib, _md5, _sha1, _sha256, _sha512, _blake2 & _sha3

import os, random, time, _hashlib, _md5, _sha1, _sha256, _sha512, _blake2, _sha3

rnd = random.SystemRandom()
def fint(): return rnd.randint(-1,10)
def fstr(): return os.urandom(rnd.randint(0,10))

def do_hash_tests(h):
  h.update(fstr())
  h.copy()
  try:
    h.digest()
    h.hexdigest()
  except TypeError:
    try:
      h.digest(fint())
      h.hexdigest(fint())
    except ValueError:
      pass

def test():
  for _ in range(9999):
    for alg in _hashlib.openssl_md_meth_names:
      _hashlib.hmac_digest(fstr(), fstr(), alg)

      try:
        _hashlib.pbkdf2_hmac(alg, fstr(), fstr(), fint())
        _hashlib.pbkdf2_hmac(alg, fstr(), fstr(), fint(), fint())
      except ValueError:
        pass

      try: _hashlib.scrypt(password=fstr(), salt=fstr(), n=fint(), r=fint(), p=fint())
      except (ValueError, TypeError, AttributeError): pass

      try:
        do_hash_tests(_hashlib.new(alg))
        do_hash_tests(_hashlib.new(alg, fstr()))
      except ValueError:
        pass

    hashes = [
      _hashlib.openssl_md5,
      _hashlib.openssl_sha1,
      _hashlib.openssl_sha224,
      _hashlib.openssl_sha256,
      _hashlib.openssl_sha384,
      _hashlib.openssl_sha512,
      _md5.md5,
      _sha1.sha1,
      _sha256.sha224,
      _sha256.sha256,
      _sha512.sha384,
      _sha512.sha512,
      _sha3.sha3_224,
      _sha3.sha3_384,
      _sha3.sha3_512,
      _sha3.shake_128,
      _sha3.shake_256
    ]

    for h in hashes:
      do_hash_tests(h())
      do_hash_tests(h(fstr()))
    
    try:
      do_hash_tests(_blake2.blake2b(
                                    fstr(),
                                    digest_size=fint(),
                                    key=fstr(),
                                    salt=fstr(),
                                    person=fstr(),
                                    fanout=fint(),
                                    depth=fint(),
                                    leaf_size=fint(),
                                    node_offset=fint(),
                                    node_depth=fint(),
                                    inner_size=fint(),
                                    last_node=fint()))
      do_hash_tests(_blake2.blake2s(
                                    fstr(),
                                    digest_size=fint(),
                                    key=fstr(),
                                    salt=fstr(),
                                    person=fstr(),
                                    fanout=fint(),
                                    depth=fint(),
                                    leaf_size=fint(),
                                    node_offset=fint(),
                                    node_depth=fint(),
                                    inner_size=fint(),
                                    last_node=fint()))
    except (ValueError, OverflowError):
      pass
    
if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
