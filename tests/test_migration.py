import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_roll_ledger

class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((ROOT/'tests/fixtures/minimal_panel/migration_daily.json').read_text())

    def test_joint_leader_confirmation_and_pressure(self):
        ledger=build_roll_ledger.build(self.rows, confirmation_days=2)
        self.assertEqual(len(ledger), 1)
        item=ledger[0]
        self.assertEqual(item['current_contract'], 'RB2405.SHF')
        self.assertEqual(item['new_contract'], 'RB2409.SHF')
        self.assertEqual(item['confirmation_start'], '2024-01-03')
        self.assertEqual(item['confirmation_end'], '2024-01-04')
        self.assertEqual(item['execution_date'], '2024-01-05')
        self.assertIsNotNone(item['migration_pressure_magnitude'])
        expected = 0.5 * (
            0.5 * ((item['new_oi_share_end'] - item['new_oi_share_start']) + (item['old_oi_share_start'] - item['old_oi_share_end']))
            + 0.5 * ((item['new_volume_share_end'] - item['new_volume_share_start']) + (item['old_volume_share_start'] - item['old_volume_share_end']))
        )
        self.assertAlmostEqual(item['migration_pressure_magnitude'], expected)
        self.assertEqual(item['status'], 'confirmed')

    def test_missing_execution_is_explicit(self):
        ledger=build_roll_ledger.build(self.rows[:-2], confirmation_days=2)
        self.assertEqual(ledger[-1]['status'], 'awaiting_execution')
        self.assertIsNone(ledger[-1]['execution_date'])

    def test_conflict_resets_confirmation_streak(self):
        rows=[dict(row) for row in self.rows]
        for row in rows:
            if row['date']=='2024-01-04' and row['symbol']=='RB2405.SHF':
                row['volume']=1000
        ledger=build_roll_ledger.build(rows, confirmation_days=2)
        self.assertEqual([item['status'] for item in ledger], ['unresolved_leader'])
        self.assertEqual(ledger[0]['date'], '2024-01-04')

if __name__=='__main__': unittest.main()
