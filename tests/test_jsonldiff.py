import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import jsonldiff


def w(tmp_path, name, rows):
    p = tmp_path / name
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return str(p)


def test_diff():
    old = {'1': {"id": 1, "a": 1}, '2': {"id": 2}}
    new = {'1': {"id": 1, "a": 2, "b": 3}, '3': {"id": 3}}
    d = jsonldiff.diff(old, new, "id")
    assert d["added"] == [{"id": 3}]
    assert d["removed"] == [{"id": 2}]
    assert d["changed"] == [{"key": 1, "fields": ["a", "b"]}]


def test_cli_diff_exit1(tmp_path, capsys):
    a = w(tmp_path, "a", [{"id": 1, "x": 1}])
    b = w(tmp_path, "b", [{"id": 1, "x": 2}])
    assert jsonldiff.main([a, b, "--key", "id", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["changed"][0]["fields"] == ["x"]


def test_cli_same_exit0(tmp_path):
    a = w(tmp_path, "a", [{"id": 1}])
    assert jsonldiff.main([a, a, "--key", "id"]) == 0


def test_missing_key(tmp_path):
    a = w(tmp_path, "a", [{"x": 1}])
    assert jsonldiff.main([a, a, "--key", "id"]) == 2
