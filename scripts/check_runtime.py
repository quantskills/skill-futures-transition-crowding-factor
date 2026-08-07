#!/usr/bin/env python3
"""Check the direct PandaData runtime without handling credentials."""
from __future__ import annotations
import argparse, importlib.util, json

def main():
    p=argparse.ArgumentParser(); p.add_argument('--method', action='append'); a=p.parse_args(); methods=a.method or []
    result={"runtime_status":"unavailable","panda_data_installed":False,"panda_data_version":None,"methods":{}}
    try:
        import panda_data
        result["panda_data_installed"]=True; result["panda_data_version"]=getattr(panda_data,'__version__',None); result["runtime_status"]="available"
        for method in methods: result["methods"][method] = callable(getattr(panda_data,method,None))
    except Exception as exc: result["error_type"]=type(exc).__name__; result["error"]="runtime import failed"
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__ == '__main__': main()
