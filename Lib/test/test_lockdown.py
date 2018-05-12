# Test lockdown and lockdownlib

import test, unittest, sys, subprocess

class LockdownTest(unittest.TestCase):
  def test_lockdown(self):
    out = subprocess.check_output(sys.executable + ' -m test.lockdown_subtest')
    failed = False
    for i, line in enumerate(out.splitlines()[:-2]):
      with self.subTest(i=i):
        self.assertTrue(line.startswith(b'PASSED'), msg=line)
        
  def test_filename_not_in_tracebacks(self):
    out = subprocess.run(sys.executable + ' -c "import lockdownlib; lockdownlib.lockdown(); raise Exception"', stderr=subprocess.PIPE).stderr
    self.assertTrue(b'File "' not in out)
    out = subprocess.run(sys.executable + ' -c "raise Exception"', stderr=subprocess.PIPE).stderr
    self.assertTrue(b'File "' in out)

def test_main():
    test.support.run_unittest(LockdownTest)

if __name__ == "__main__":
    test_main()
