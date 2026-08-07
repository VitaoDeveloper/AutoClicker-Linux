import os
import tempfile

from app.config import load_config, save_config, _config_file, _xdg_config_home


def test_config_file_respects_xdg_config_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    expected = tmp_path / "autoclicker" / "config.json"
    assert _config_file() == expected


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    original = {"interval": 0.5, "button": 2, "amount": 10, "hotkey": "f7"}
    save_config(original)
    loaded = load_config()
    assert loaded == original


def test_load_returns_defaults_when_no_file(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    loaded = load_config()
    assert loaded["interval"] == 0.1
    assert loaded["hotkey"] == "f6"
    assert _config_file().exists()


def test_migrate_from_legacy(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    legacy = tmp_path / "repo_root" / "config.json"
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_text('{"interval": 0.3, "button": 3, "amount": 5, "hotkey": "f8"}')

    monkeypatch.setattr("app.config._legacy_config_file", lambda: legacy)
    loaded = load_config()
    assert loaded["interval"] == 0.3
    assert _config_file().exists()
