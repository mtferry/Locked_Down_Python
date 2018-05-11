# Test lockdown and lockdownlib

import test, unittest, sys, subprocess

class LockdownTest(unittest.TestCase):
  def test_lockdown(self):
    out = subprocess.check_output(sys.executable + ' -m test.lockdown_subtest')
    failed = False
    for i, line in enumerate(out.splitlines()[:-2]):
      with self.subTest(i=i):
        self.assertTrue(line.startswith(b'PASSED'), msg=line)

def test_main():
    test.support.run_unittest(LockdownTest)

if __name__ == "__main__":
    test_main()
