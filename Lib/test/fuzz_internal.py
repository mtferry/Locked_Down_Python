# Fuzz Tests for _ast, _opcode

import test.fuzzhelper as fh
import _ast, _opcode

def test():
  for _ in range(9999):
    fh.check(_opcode, valid_inputs = [((fh.int,),{}), ((fh.int, fh.object),{})], expected_exceptions = (TypeError, ValueError))
    fh.check(_ast, valid_inputs = [((),{})], expected_exceptions = (TypeError, ValueError))

if __name__ == '__main__': fh.do_test_loop(test)
