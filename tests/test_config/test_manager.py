import json
from pathlib import Path
import pytest
from src.config.manager import ConfigManager


class TestConfigManager:
    """Test suite for the ConfigManager class."""

    def test_default_path_resolution(self):
        """Test that the default config path is resolved correctly."""
        manager = ConfigManager()
        expected_path = Path.home() / ".weekly"
        assert manager.config_path == expected_path

    def test_custom_path_resolution(self, tmp_path):
        """Test that a custom config path is resolved correctly."""
        custom_path = tmp_path / "my_config.json"
        manager = ConfigManager(path=str(custom_path))
        assert manager.config_path == custom_path

    def test_load_nonexistent_config(self, tmp_path):
        """Test that loading a non-existent config file returns an empty dict."""
        manager = ConfigManager(path=str(tmp_path / "nonexistent.json"))
        assert manager.config == {}

    def test_add_and_get_config(self, tmp_path):
        """Test adding and retrieving a configuration key-value pair."""
        config_file = tmp_path / "test.json"
        manager = ConfigManager(path=str(config_file))

        manager.add("user.name", "John Doe")
        assert manager.get("user.name") == "John Doe"

        # Verify it was saved to the file
        reloaded_manager = ConfigManager(path=str(config_file))
        assert reloaded_manager.get("user.name") == "John Doe"

    def test_update_config(self, tmp_path):
        """Test updating an existing configuration key."""
        config_file = tmp_path / "test.json"
        manager = ConfigManager(path=str(config_file))

        manager.add("user.name", "John Doe")
        manager.add("user.name", "Jane Doe")
        assert manager.get("user.name") == "Jane Doe"

    def test_remove_config(self, tmp_path):
        """Test removing a configuration key."""
        config_file = tmp_path / "test.json"
        manager = ConfigManager(path=str(config_file))

        manager.add("user.email", "test@example.com")
        assert "user.email" in manager.config

        manager.remove("user.email")
        assert "user.email" not in manager.config
        assert manager.get("user.email") is None

        # Verify it was removed from the file
        reloaded_manager = ConfigManager(path=str(config_file))
        assert "user.email" not in reloaded_manager.config

    def test_remove_nonexistent_key(self, tmp_path, capsys):
        """Test that removing a nonexistent key prints a message."""
        config_file = tmp_path / "test.json"
        manager = ConfigManager(path=str(config_file))

        manager.remove("nonexistent.key")
        captured = capsys.readouterr()
        assert "Configuration key not found" in captured.out

    def test_load_malformed_config(self, tmp_path):
        """Test loading a malformed JSON file."""
        config_file = tmp_path / "malformed.json"
        with open(config_file, "w") as f:
            f.write("{'invalid_json': ")

        manager = ConfigManager(path=str(config_file))
        assert manager.config == {}
