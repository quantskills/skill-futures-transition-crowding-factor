import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class RuntimeTests(unittest.TestCase):
    def test_runtime_reports_status_without_credentials(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/check_runtime.py'),'--method','get_future_daily'],capture_output=True,text=True,check=True)
        self.assertIn('runtime_status',p.stdout)
        self.assertNotIn('password',p.stdout.lower())
        self.assertNotIn('token',p.stdout.lower())

if __name__=='__main__': unittest.main()
