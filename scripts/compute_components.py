#!/usr/bin/env python3
"""Compute contract-level HHI and migration components from normalized rows."""
from __future__ import annotations
import argparse, json, math
from collections import defaultdict
from pathlib import Path


def hhi(values):
    total = sum(max(float(v), 0.0) for v in values)
    if total <= 0: return None
    return sum((max(float(v), 0.0) / total) ** 2 for v in values)


def percentile_scores(values):
    ordered = sorted(values, key=lambda x: (-x[1], x[0]))
    n = len(ordered)
    if n <= 1: return {key: 1.0 for key, _ in ordered}
    return {key: 1 - rank / (n - 1) for rank, (key, _) in enumerate(ordered)}


def compute(rows, min_active_contracts=3, candidate_k=3):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["date"], row["underlying_symbol"])].append(row)
    output = []
    for (date, instrument), items in sorted(grouped.items()):
        eligible = [r for r in items if r.get("eligible", True)]
        oi_active = [r for r in eligible if float(r.get("open_interest", 0) or 0) > 0]
        vol_active = [r for r in eligible if float(r.get("volume", 0) or 0) > 0]
        record = {"date": date, "underlying_symbol": instrument,
                  "eligible_contract_count": len(eligible),
                  "oi_active_contract_count": len(oi_active),
                  "volume_active_contract_count": len(vol_active),
                  "oi_hhi_all_eligible": hhi([r.get("open_interest", 0) for r in eligible]),
                  "volume_hhi_all_eligible": hhi([r.get("volume", 0) for r in eligible]),
                  "oi_hhi_active": hhi([r.get("open_interest", 0) for r in oi_active]) if len(oi_active) >= min_active_contracts else None,
                  "volume_hhi_active": hhi([r.get("volume", 0) for r in vol_active]) if len(vol_active) >= min_active_contracts else None}
        activity = []
        oi_scores = percentile_scores([(r["symbol"], float(r.get("open_interest", 0) or 0)) for r in eligible])
        vol_scores = percentile_scores([(r["symbol"], float(r.get("volume", 0) or 0)) for r in eligible])
        for r in eligible:
            if r.get("open_interest") is None or r.get("volume") is None: continue
            activity.append((r["symbol"], 0.5 * oi_scores[r["symbol"]] + 0.5 * vol_scores[r["symbol"]]))
        activity.sort(key=lambda x: (-x[1], x[0]))
        record["candidate_pool"] = [symbol for symbol, _ in activity[:candidate_k]]
        record["provider_dominant_id"] = next((r.get("dominant_id") for r in items if r.get("dominant_id")), None)
        output.append(record)
    return output


def main():
    p = argparse.ArgumentParser(); p.add_argument("input", type=Path); p.add_argument("--out", type=Path); p.add_argument("--min-active", type=int, default=3); p.add_argument("--candidate-k", type=int, default=3)
    a = p.parse_args(); rows = json.loads(a.input.read_text(encoding="utf-8")); result = compute(rows, a.min_active, a.candidate_k); text=json.dumps(result, ensure_ascii=False, indent=2)+"\n"
    if a.out: a.out.write_text(text, encoding="utf-8")
    else: print(text, end="")
if __name__ == "__main__": main()
