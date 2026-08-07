import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import robust_standardize

class StandardizeTests(unittest.TestCase):
    def test_insufficient_history_is_not_filled(self):
        rows=[{"date":f"2024-01-{i:02d}","underlying_symbol":"RB","x":float(i)} for i in range(1,5)]
        result=robust_standardize.standardize(rows,'x',window=5,min_history_ratio=.8)
        self.assertTrue(all(row['x_ts_z'] is None for row in result))
        self.assertTrue(all(row['x_ts_status']=='insufficient_history' for row in result))
    def test_zero_dispersion_is_unavailable(self):
        history=[{"date":f"2024-01-{i:02d}","underlying_symbol":"RB","x":1.0} for i in range(1,7)]
        result=robust_standardize.standardize(history,'x',window=5,min_history_ratio=.8)
        self.assertEqual(result[-1]['x_ts_status'],'zero_dispersion')

if __name__=='__main__': unittest.main()
