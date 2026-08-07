#!/usr/bin/env python3
"""Build a declared open-to-open label from supplied price rows."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build(rows, horizon=5):
    by_symbol = {}
    for row in rows:
        by_symbol.setdefault(row["underlying_symbol"], []).append(row)
    output = []
    for symbol, items in by_symbol.items():
        items = sorted(items, key=lambda row: row["date"])
        for index, signal in enumerate(items):
            entry_index = index + 1
            exit_index = index + 1 + horizon
            item = {
                "signal_date": signal["date"],
                "underlying_symbol": symbol,
                "horizon": horizon,
                "label_status": "not_available" if exit_index >= len(items) else "available",
            }
            if exit_index < len(items):
                entry_price = items[entry_index].get("open")
                exit_price = items[exit_index].get("open")
                item.update({"entry_date": items[entry_index]["date"], "exit_date": items[exit_index]["date"], "entry_price": entry_price, "exit_price": exit_price})
                if entry_price is None or exit_price is None:
                    item["label_status"] = "insufficient_price_data"
                else:
                    item["raw_price_return"] = exit_price / entry_price - 1
            output.append(item)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--horizon", type=int, default=5)
    args = parser.parse_args()
    value = build(json.loads(args.input.read_text(encoding="utf-8")), args.horizon)
    args.out.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
