#!/usr/bin/env python3
"""Validate that a frozen primary-test configuration has required declarations."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def validate(value):
    required=['data_source','confirmation_days','candidate_pool','standardization','primary_test']
    errors=[f'missing:{x}' for x in required if x not in value]
    primary=value.get('primary_test',{})
    if primary and primary.get('factor')!='crowding_reversal_core': errors.append('primary_test.factor')
    return errors

def main():
    p=argparse.ArgumentParser(); p.add_argument('config',type=Path); a=p.parse_args(); errors=validate(json.loads(a.config.read_text(encoding='utf-8')))
    if errors:
        print('\n'.join('ERROR '+e for e in errors)); raise SystemExit(1)
    print('freeze configuration validation passed')
if __name__=='__main__': main()
