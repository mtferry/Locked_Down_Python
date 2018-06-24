# Fuzz Tests for builtins, _operator

import test.fuzzhelper as fh
import builtins, _operator

def test():
  for _ in range(99):
    fh.check(builtins,
             valid_inputs = [
                            ((),{}),
                            ((fh.str,),{}),
                            ((fh.bytes,),{}),
                            ((fh.list,),{}),
                            ((fh.list,fh.list),{})
                            ],
             expected_exceptions = (TypeError, ValueError, AttributeError, IndexError, RuntimeError, SyntaxError, NameError, KeyError),
             dir_func = lambda i: set(dir(i))-{'__import__', 'help', 'exit', 'quit', 'input', 'history', 'open', 'breakpoint', 'license','copyright', 'print', 'credits'})

    fh.check(_operator,
             valid_inputs = [
                             ((fh.object,),{}),
                             ((fh.object, fh.object),{}),
                             ((fh.list, fh.object),{}),
                             ((fh.dict, fh.object),{})
                            ],
             expected_exceptions = (TypeError, ValueError, IndexError, ZeroDivisionError, KeyError))

if __name__ == '__main__': fh.do_test_loop(test)
