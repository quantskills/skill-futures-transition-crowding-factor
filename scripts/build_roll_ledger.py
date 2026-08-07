#!/usr/bin/env python3
"""Create a conservative migration ledger from pre-confirmed transition rows."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def build(rows, confirmation_days=2):
    output=[]
    for row in rows:
        item=dict(row); item['confirmation_days']=confirmation_days
        required=('current_contract','new_contract','confirmation_start','confirmation_end','execution_date')
        item['status']='confirmed' if all(row.get(k) for k in required) else 'unresolved'
        if item['status']!='confirmed': item['execution_price_status']='not_available'
        output.append(item)
    return output

def main():
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--out',type=Path,required=True); p.add_argument('--confirmation-days',type=int,default=2); a=p.parse_args(); a.out.write_text(json.dumps(build(json.loads(a.input.read_text(encoding='utf-8')),a.confirmation_days),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
