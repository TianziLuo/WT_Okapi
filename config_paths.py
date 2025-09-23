import sys
from pathlib import Path
import configparser

# Base path depends on runtime environment
if getattr(sys, "frozen", False):  # exe 打包环境
    _base_path = Path(sys.executable).parent
else:  # 开发环境
    _base_path = Path(__file__).parent

# Path to the configuration file
_config_path = _base_path / "WT_config.ini"

# Load config
config = configparser.ConfigParser()
config.optionxform = str  # 保持 key 的大小写
read_files = config.read(_config_path, encoding="utf-8")

if not read_files:
    raise FileNotFoundError(f"Configuration file not found: {_config_path}")

def get_wt_paths():
    """Return all Common + WT paths as pathlib.Path dict"""
    paths = dict(config.items("Common"))
    paths.update(config.items("WT"))
    return {k: Path(v) for k, v in paths.items()}


