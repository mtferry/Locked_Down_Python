# Test properties of bool promised by PEP 285

import test, unittest, sys, subprocess

class LockdownTest(unittest.TestCase):
  def test_lockdown(self):
    out = subprocess.check_output(sys.executable + ' -m test.lockdown_subtest')
    failed = False
    for line in out.splitlines()[:-2]:
      if line.startswith(b'FAILED'):
        failed = True
        print('  ', line)
    self.assertFalse(failed)

def test_main():
    test.support.run_unittest(LockdownTest)

if __name__ == "__main__":
    test_main()
