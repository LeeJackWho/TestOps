"""框架自测：配置模块"""
import os

from Config.setting import BASE_DIR, LOG_DIR, REPORT_DIR


def test_base_dir_is_repo_root():
    """BASE_DIR 应为仓库根目录：包含 Config/ 与 TestDatas/ 等标志性子目录"""
    assert os.path.isabs(BASE_DIR)
    assert os.path.isdir(os.path.join(BASE_DIR, "Config"))
    assert os.path.isdir(os.path.join(BASE_DIR, "TestDatas"))


def test_derived_dirs_live_under_base_dir():
    """LOG_DIR / REPORT_DIR 必须挂在 BASE_DIR 之下"""
    for path in (LOG_DIR, REPORT_DIR):
        assert os.path.isabs(path)
        assert os.path.commonpath([BASE_DIR, path]) == BASE_DIR
