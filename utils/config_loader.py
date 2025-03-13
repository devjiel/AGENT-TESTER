"""
Configuration loader utility
"""
import os
import yaml
from typing import Dict, Any

class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.load_config()

    def load_config(self, config_path: str = "config.yaml") -> None:
        """Load configuration from yaml file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
            
        # Ensure required paths exist
        self._create_directories()

    def _create_directories(self) -> None:
        """Create required directories if they don't exist"""
        data_dir = self.get_data_dir()
        screenshots_dir = self.get_screenshots_dir()
        analyses_dir = self.get_analyses_dir()
        
        directories = [data_dir, screenshots_dir, analyses_dir]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def get_config(self) -> Dict[str, Any]:
        """Get the loaded configuration"""
        if self._config is None:
            self.load_config()
        if self._config is None:
            # return default config
            return {"paths": {"data_dir": "data"}, "browser": {}}
        return self._config

    @property
    def paths(self) -> Dict[str, str]:
        """Get paths configuration"""
        return self.get_config()['paths']

    @property
    def browser(self) -> Dict[str, Any]:
        """Get browser configuration"""
        return self.get_config()['browser']
        
    def get_data_dir(self) -> str:
        """Get the data directory path"""
        return self.paths['data_dir']
        
    def get_screenshots_dir(self) -> str:
        """Get the screenshots directory path"""
        return os.path.join(self.get_data_dir(), 'screenshots')
        
    def get_analyses_dir(self) -> str:
        """Get the analyses directory path"""
        return os.path.join(self.get_data_dir(), 'analyses')
        
    def get_ui_description_path(self) -> str:
        """Get the ui description file path"""
        return os.path.join(self.get_analyses_dir(), 'ui_description.txt')