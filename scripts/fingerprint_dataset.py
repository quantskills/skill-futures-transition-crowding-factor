#!/usr/bin/env python3
"""Fingerprint normalized dataset metadata and content without credentials."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=str)
def main():
    p=argparse.ArgumentParser(); p.add_argument('input',type=Path); a=p.parse_args(); raw=a.input.read_text(encoding='utf-8'); print(json.dumps({'content_fingerprint':'sha256:'+hashlib.sha256(canonical(json.loads(raw)).encode()).hexdigest(),'file_sha256':'sha256:'+hashlib.sha256(raw.encode()).hexdigest()},indent=2))
if __name__=='__main__': main()
