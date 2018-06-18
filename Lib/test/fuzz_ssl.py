# Fuzz Tests for ssl

import os, random, time, struct, socket, _ssl

rnd = random.SystemRandom()
def fint(): return rnd.randint(0,3)
def fstr(): return os.urandom(rnd.randint(0,20))
def flst(): return [fstr() for _ in range(fint())]
def fdouble(): return struct.unpack('d', os.urandom(8))[0]
def flong(): return struct.unpack('i', os.urandom(4))[0]
def fbool(): return not rnd.randint(0,1)

def test():
  for _ in range(9999):
    bio = _ssl.MemoryBIO()
    for _ in range(fint()):
      if fint():
        try: bio.write(fstr())
        except _ssl.SSLError: pass
      if fint(): bio.read()
      if fint(): bio.write_eof()
      bio.pending
      bio.eof

    _ssl.RAND_add(fstr(), fdouble())
    _ssl.RAND_status()
    try:
      _ssl.RAND_bytes(fint())
      _ssl.RAND_pseudo_bytes(fint())
    except _ssl.SSLError:
      pass

    while True:
      try: ctx = _ssl._SSLContext(rnd.randint(-1,20)) ; break
      except ValueError: continue
    
    try: ctx.set_ciphers(str(fstr()))
    except _ssl.SSLError: pass
    
    try: ctx.set_alpn_protocols(flst())
    except (AttributeError, _ssl.SSLError): pass
    
    try: ctx.set_npn_protocols(flst())
    except (AttributeError, _ssl.SSLError): pass

    try: ctx.set_ecdh_curve(fstr())
    except (ValueError, _ssl.SSLError): pass

    ctx.get_ciphers()
    ctx.check_hostname
    ctx.check_hostname = fbool()
    ctx._host_flags
    ctx._host_flags = flong()
    ctx.minimum_version
    try: ctx.minimum_version = flong()
    except (ValueError, _ssl.SSLError): pass
    ctx.maximum_version
    try: ctx.maximum_version = flong()
    except (ValueError, _ssl.SSLError): pass
    ctx.sni_callback
    try: ctx.sni_callback = flong
    except (ValueError, _ssl.SSLError): pass
    ctx.options
    ctx.options = flong()
    ctx.protocol
    ctx.verify_flags
    ctx.verify_flags = flong()
    ctx.verify_mode
    try: ctx.verify_mode = flong()
    except (ValueError, _ssl.SSLError): pass

    sock = socket.socket()
    sock = ctx._wrap_socket(sock, fbool())
    sock.compression()
    sock.cipher()
    sock.shared_ciphers()
    sock.version()
    sock.selected_alpn_protocol()
    sock.selected_npn_protocol()
    
    try: sock.do_handshake()
    except _ssl.SSLError: pass
    
    try: sock.write(fstr())
    except _ssl.SSLError: pass
    
    try: sock.read(fint())
    except _ssl.SSLError: pass
    
    sock.pending()
    sock.context
    sock.server_side
    sock.server_hostname
    sock.owner
    sock.session
    sock.session_reused

    try: sock.shutdown()
    except _ssl.SSLError: pass

if __name__ == '__main__':
  print('Start Time:', time.ctime())
  for i in range(1,99999):
    test()
    print('End of Iteration', i, '-', time.ctime())
