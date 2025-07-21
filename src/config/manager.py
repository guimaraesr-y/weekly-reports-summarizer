import os
import json
from pathlib import Path


class ConfigManager:
    """Manages user preferences in a JSON configuration file."""

    def __init__(self, path: str = None):
        """
        Initializes the ConfigManager.

        Args:
            path (str, optional): The path to the config file.
                                  Defaults to ~/.weekly.
        """
        self.config_path = self._resolve_path(path)
        self.config = self._load_config()

    def _resolve_path(self, path: str) -> Path:
        """
        Resolves the configuration file path.

        Args:
            path (str): The path provided by the user.

        Returns:
            Path: The resolved absolute path to the config file.
        """
        if path:
            return Path(path).expanduser().resolve()
        return Path.home() / ".weekly"

    def _load_config(self) -> dict:
        """
        Loads the configuration from the JSON file.

        Returns:
            dict: The loaded configuration.
        """
        if not self.config_path.exists():
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_config(self):
        """Saves the current configuration to the JSON file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except OSError as e:
            print(f"Error saving configuration: {e}")

    def add(self, key: str, value: any):
        """
        Adds or updates a configuration key-value pair.

        Args:
            key (str): The configuration key.
            value (any): The configuration value.
        """
        self.config[key] = value
        self._save_config()
        print(f"Updated configuration: '{key}' = '{value}'")

    def remove(self, key: str):
        """
        Removes a configuration key.

        Args:
            key (str): The key to remove.
        """
        if key in self.config:
            del self.config[key]
            self._save_config()
            print(f"Removed configuration key: '{key}'")
        else:
            print(f"Configuration key not found: '{key}'")

    def get(self, key: str, default: any = None) -> any:
        """
        Gets a configuration value.

        Args:
            key (str): The key to retrieve.
            default (any, optional): The default value to return if the key
                                     is not found. Defaults to None.

        Returns:
            any: The configuration value.
        """
        return self.config.get(key, default)
