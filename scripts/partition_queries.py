#!/usr/bin/env python3
"""Partition a declared date range into calendar-year query partitions."""
from __future__ import annotations
import argparse, datetime as dt, json, re
from pathlib import Path

def partition(start,end):
    s=dt.date.fromisoformat(start); e=dt.date.fromisoformat(end); out=[]; cur=s
    while cur<=e:
        stop=min(dt.date(cur.year,12,31),e); out.append({"partition_id":f"{cur.year}","start_date":cur.isoformat(),"end_date":stop.isoformat()}); cur=stop+dt.timedelta(days=1)
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument('config',type=Path); p.add_argument('--start',required=True); p.add_argument('--end',required=True); a=p.parse_args(); print(json.dumps({"boundary":"calendar_year","partitions":partition(a.start,a.end)},indent=2))
if __name__=='__main__': main()
