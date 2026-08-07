import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import compute_components

class ComponentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((ROOT/'tests/fixtures/minimal_panel/contract_daily.json').read_text())
    def test_active_hhi_excludes_zero_activity(self):
        rows=self.rows + [{"date":"2024-01-02","symbol":"RB2412.SHF","underlying_symbol":"RB","eligible":True,"volume":0,"open_interest":0}]
        result=compute_components.compute(rows, min_active_contracts=3)[0]
        self.assertEqual(result['oi_active_contract_count'],4)
        self.assertGreater(result['oi_hhi_active'],0)
    def test_candidate_pool_is_deterministic(self):
        result=compute_components.compute(self.rows, candidate_k=3)
        self.assertEqual(result[0]['candidate_pool'], ['RB2405.SHF','RB2409.SHF','RB2410.SHF'])
        self.assertEqual(result[0]['provider_dominant_id'], 'RB2405.SHF')

if __name__=='__main__': unittest.main()
