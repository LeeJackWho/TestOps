# 数据文件读取

import yaml
import json
from Config.setting import BASE_DIR

def load_yaml(file_path: str) -> dict:
    """读取YAML测试数据"""
    with open(f"{BASE_DIR}/TestDatas/{file_path}", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_json(file_path: str) -> dict:
    """读取JSON配置文件"""
    with open(f"{BASE_DIR}/TestDatas/{file_path}", 'r') as f:
        return json.load(f)