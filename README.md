# jsonldiff

Zero-dependency Python 3 CLI that compares two JSON Lines files by a key field and reports added, removed and changed records (with changed field names).

## Usage

    python3 jsonldiff.py old.jsonl new.jsonl --key id [--json]

Example output:

    + 3
    - 2
    ~ 1: a, b

`+` added, `-` removed, `~` changed (field names listed). `--json` prints `{"added": [...], "removed": [...], "changed": [{"key":..., "fields":[...]}]}`.

Exit codes: 0 no differences, 1 differences, 2 error (bad input/missing key).

## Tests

    python3 -m pytest

## Related tools

- [jsonlq](https://github.com/hal5000-openclaw/jsonlq) – query JSONL files
- [envcheck](https://github.com/hal5000-openclaw/envcheck) – validate .env files
