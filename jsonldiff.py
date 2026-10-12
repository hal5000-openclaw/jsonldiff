#!/usr/bin/env python3
"""Compare two JSON Lines files by a key field."""
import argparse
import json
import sys


def load(path, key):
    records = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{n}: invalid JSON: {e}")
            if not isinstance(obj, dict) or key not in obj:
                raise ValueError(f"{path}:{n}: missing key '{key}'")
            records[json.dumps(obj[key], sort_keys=True)] = obj
    return records


def diff(old, new, key):
    added = [new[k] for k in new if k not in old]
    removed = [old[k] for k in old if k not in new]
    changed = []
    for k in old:
        if k in new and old[k] != new[k]:
            fields = sorted(f for f in set(old[k]) | set(new[k])
                            if old[k].get(f, _M) != new[k].get(f, _M))
            changed.append({"key": old[k][key], "fields": fields})
    return {"added": added, "removed": removed, "changed": changed}


_M = object()


def main(argv=None):
    p = argparse.ArgumentParser(prog="jsonldiff", description=__doc__)
    p.add_argument("old")
    p.add_argument("new")
    p.add_argument("--key", required=True, help="key field name")
    p.add_argument("--json", action="store_true", help="JSON output")
    a = p.parse_args(argv)
    try:
        d = diff(load(a.old, a.key), load(a.new, a.key), a.key)
    except (OSError, ValueError) as e:
        print(f"jsonldiff: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(d))
    else:
        for r in d["added"]:
            print(f"+ {json.dumps(r[a.key])}")
        for r in d["removed"]:
            print(f"- {json.dumps(r[a.key])}")
        for c in d["changed"]:
            print(f"~ {json.dumps(c['key'])}: {', '.join(c['fields'])}")
    return 1 if any(d.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
