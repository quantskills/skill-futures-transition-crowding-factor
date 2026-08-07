#!/usr/bin/env python3
"""Robust rolling and cross-sectional median/MAD standardization."""
from __future__ import annotations
import argparse, json, math
from collections import defaultdict, deque
from pathlib import Path

SCALE = 1.4826

def robust_z(value, history, tolerance=1e-12, clip=5.0):
    if value is None or len(history) == 0: return None, "unavailable"
    ordered=sorted(history); n=len(ordered); med=ordered[n//2] if n%2 else (ordered[n//2-1]+ordered[n//2])/2
    deviations=sorted(abs(x-med) for x in ordered); m=deviations[len(deviations)//2] if len(deviations)%2 else (deviations[len(deviations)//2-1]+deviations[len(deviations)//2])/2
    if SCALE*m <= tolerance: return None, "zero_dispersion"
    z=(value-med)/(SCALE*m); return max(-clip, min(clip, z)), "available"

def standardize(rows, field, window=252, min_history_ratio=.8, tolerance=1e-12, clip=5.):
    by_inst=defaultdict(list)
    for row in sorted(rows, key=lambda r:(r.get("underlying_symbol", ""), r["date"])): by_inst[row.get("underlying_symbol", "")].append(row)
    out=[]
    for inst, items in by_inst.items():
        history=deque(maxlen=window)
        for row in items:
            value=row.get(field); needed=math.ceil(window*min_history_ratio)
            ts=None; status="insufficient_history"
            if value is not None and len(history)>=needed: ts,status=robust_z(float(value), list(history), tolerance, clip)
            new=dict(row); new[field+"_ts_z"]=ts; new[field+"_ts_status"]=status
            if value is not None and math.isfinite(float(value)):
                history.append(float(value))
            out.append(new)
    dates=defaultdict(list)
    for row in out:
        if row.get(field+"_ts_z") is not None and math.isfinite(row[field+"_ts_z"]): dates[row["date"]].append(row)
    for row in out:
        peers=dates[row["date"]]; vals=[x[field+"_ts_z"] for x in peers]; z,status=robust_z(row.get(field+"_ts_z"), vals, tolerance, clip) if row.get(field+"_ts_z") is not None else (None,"unavailable"); row[field+"_cs_z"]=z; row[field+"_cs_status"]=status
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); p.add_argument("field"); p.add_argument("--out",type=Path); p.add_argument("--window",type=int,default=252); a=p.parse_args(); rows=json.loads(a.input.read_text(encoding="utf-8")); result=standardize(rows,a.field,a.window); text=json.dumps(result,ensure_ascii=False,indent=2)+"\n"; a.out.write_text(text,encoding="utf-8") if a.out else print(text,end="")
if __name__ == "__main__": main()
