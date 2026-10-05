"""框架自测：YAML/JSON 数据加载器（数据驱动层的核心）"""
import json

import pytest

from Common.read_file import load_yaml, load_json


def test_load_yaml_returns_dict():
    data = load_yaml("api_test_data.yaml")
    assert isinstance(data, dict)
    assert "test_data" in data


def test_load_yaml_parses_nested_structure():
    data = load_yaml("api_test_data.yaml")
    endpoint = data["test_data"]["endpoint1"]
    assert endpoint["expected"]["status_code"] == 200


def test_load_yaml_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_yaml("__not_exist__.yaml")


def test_load_json_roundtrip(tmp_path, monkeypatch):
    # load_json 以 BASE_DIR/TestDatas 为根，用临时目录验证解析逻辑
    payload = {"ok": True, "items": [1, 2, 3]}
    datas = tmp_path / "TestDatas"
    datas.mkdir()
    (datas / "tmp_data.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr("Common.read_file.BASE_DIR", str(tmp_path))
    assert load_json("tmp_data.json") == payload
