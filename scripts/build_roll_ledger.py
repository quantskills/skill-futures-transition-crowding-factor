#!/usr/bin/env python3
"""Confirm contract migration and compute an auditable roll ledger."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import compute_components


def _leader(items, field, candidates):
    active = [
        row for row in items
        if row.get("eligible", True)
        and row["symbol"] in candidates
        and float(row.get(field, 0) or 0) > 0
    ]
    if not active:
        return None
    return sorted(active, key=lambda row: (-float(row.get(field, 0) or 0), row["symbol"]))[0]["symbol"]


def _shares(items, symbol):
    active = [row for row in items if row.get("eligible", True) and float(row.get("open_interest", 0) or 0) > 0 and float(row.get("volume", 0) or 0) > 0]
    oi_total = sum(float(row.get("open_interest", 0) or 0) for row in active)
    vol_total = sum(float(row.get("volume", 0) or 0) for row in active)
    row = next((item for item in active if item["symbol"] == symbol), None)
    if row is None or oi_total <= 0 or vol_total <= 0:
        return None, None
    return float(row["open_interest"]) / oi_total, float(row["volume"]) / vol_total


def build(rows, confirmation_days=2, candidate_k=3):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["underlying_symbol"], row["date"])].append(row)
    dates_by_instrument = defaultdict(list)
    for instrument, date in grouped:
        dates_by_instrument[instrument].append(date)
    output = []
    for instrument, dates in sorted(dates_by_instrument.items()):
        dates.sort()
        joint = {}
        candidates_by_date = {}
        for date in dates:
            items = grouped[(instrument, date)]
            components = compute_components.compute(items, min_active_contracts=1, candidate_k=candidate_k)[0]
            candidates = set(components["candidate_pool"])
            candidates_by_date[date] = sorted(candidates)
            oi_leader = _leader(items, "open_interest", candidates)
            vol_leader = _leader(items, "volume", candidates)
            joint[date] = oi_leader if oi_leader and oi_leader == vol_leader else None
            if oi_leader and vol_leader and oi_leader != vol_leader:
                output.append({
                    "underlying_symbol": instrument,
                    "date": date,
                    "candidate_pool": sorted(candidates),
                    "oi_leader": oi_leader,
                    "volume_leader": vol_leader,
                    "status": "unresolved_leader",
                })
        current = next((joint[date] for date in dates if joint[date]), None)
        streak_contract = None
        streak_dates = []
        for index, date in enumerate(dates):
            candidate = joint[date]
            if not current or not candidate or candidate == current:
                streak_contract, streak_dates = None, []
                continue
            if candidate != streak_contract:
                streak_contract, streak_dates = candidate, []
            streak_dates.append(date)
            if len(streak_dates) < confirmation_days:
                continue
            start_date, end_date = streak_dates[0], streak_dates[-1]
            execution_date = dates[index + 1] if index + 1 < len(dates) else None
            old_oi_start, old_vol_start = _shares(grouped[(instrument, start_date)], current)
            new_oi_start, new_vol_start = _shares(grouped[(instrument, start_date)], candidate)
            old_oi_end, old_vol_end = _shares(grouped[(instrument, end_date)], current)
            new_oi_end, new_vol_end = _shares(grouped[(instrument, end_date)], candidate)
            values = [old_oi_start, old_vol_start, new_oi_start, new_vol_start, old_oi_end, old_vol_end, new_oi_end, new_vol_end]
            pressure = None
            if all(value is not None for value in values):
                oi_transfer = 0.5 * ((new_oi_end - new_oi_start) + (old_oi_start - old_oi_end))
                vol_transfer = 0.5 * ((new_vol_end - new_vol_start) + (old_vol_start - old_vol_end))
                pressure = 0.5 * (oi_transfer + vol_transfer)
            output.append({
                "underlying_symbol": instrument, "current_contract": current, "new_contract": candidate,
                "candidate_pool": candidates_by_date[end_date],
                "confirmation_start": start_date, "confirmation_end": end_date, "execution_date": execution_date,
                "confirmation_days": confirmation_days,
                "old_oi_share_start": old_oi_start, "new_oi_share_start": new_oi_start,
                "old_oi_share_end": old_oi_end, "new_oi_share_end": new_oi_end,
                "old_volume_share_start": old_vol_start, "new_volume_share_start": new_vol_start,
                "old_volume_share_end": old_vol_end, "new_volume_share_end": new_vol_end,
                "migration_pressure_magnitude": pressure,
                "migration_pressure_status": "available" if pressure is not None else "not_available",
                "provider_dominant_start": next((r.get("dominant_id") for r in grouped[(instrument, start_date)] if r.get("dominant_id")), None),
                "provider_dominant_end": next((r.get("dominant_id") for r in grouped[(instrument, end_date)] if r.get("dominant_id")), None),
                "status": "confirmed" if execution_date else "awaiting_execution",
            })
            current, streak_contract, streak_dates = candidate, None, []
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--confirmation-days", type=int, default=2)
    parser.add_argument("--candidate-k", type=int, default=3)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))
    args.out.write_text(
        json.dumps(build(rows, args.confirmation_days, args.candidate_k), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
