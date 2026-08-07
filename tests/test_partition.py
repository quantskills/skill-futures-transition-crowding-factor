import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

class PartitionTests(unittest.TestCase):
    def test_calendar_partitions_are_non_overlapping(self):
        p=subprocess.run([PY,str(ROOT/'scripts/partition_queries.py'),'examples/config.example.yaml','--start','2024-06-01','--end','2025-02-01'],capture_output=True,text=True,check=True)
        data=json.loads(p.stdout)
        self.assertEqual(data['partitions'][0]['start_date'],'2024-06-01')
        self.assertEqual(data['partitions'][-1]['end_date'],'2025-02-01')
        self.assertEqual(len(data['partitions']),2)

if __name__=='__main__': unittest.main()
