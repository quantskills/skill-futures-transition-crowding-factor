#!/usr/bin/env python3
"""Build a factor panel from component rows without dynamic component reweighting."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def build(rows):
    out=[]
    required=('oi_hhi_active_cs_z','volume_hhi_active_cs_z','migration_pressure_magnitude_cs_z')
    for row in rows:
        values=[row.get(key) for key in required]
        available=all(isinstance(v,(int,float)) for v in values)
        item=dict(row)
        item['crowding_score_core']=sum(values)/3 if available else None
        item['crowding_reversal_core']=-item['crowding_score_core'] if available else None
        item['factor_status']='available' if available else 'not_available'
        item['core_component_count']=sum(isinstance(v,(int,float)) for v in values)
        out.append(item)
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--out',type=Path,required=True); a=p.parse_args(); a.out.write_text(json.dumps(build(json.loads(a.input.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
