import tomllib
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """加载TOML配置文件"""
    config_path = Path(__file__).parent / "config.toml"
    if not config_path.exists():
        raise FileNotFoundError("配置文件 config.toml 不存在，请创建")
    
    with open(config_path, "rb") as f:
        return tomllib.load(f)

# 全局配置字典
settings = load_config()
