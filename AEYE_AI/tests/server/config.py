from dataclasses import dataclass, field

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from enum import Enum


from dataclasses import dataclass, field, is_dataclass, asdict
import os
import yaml
import importlib
from enum import Enum
from pathlib import Path
import torch
import numpy as np
from typing import Any, Dict, Union
import types

class PostMode(str, Enum):
    RAND = "rand"
    REAL = "real"
    
class ContentType(str, Enum):
    JSON = "application/json"
    OCTET = "application/octet-stream"
    MULTIPART = "multipart/form-data"


@dataclass
class SERVERConfig:
    content_type : str = 'application/octet-stream'
    img_path : str = '../data/samples/image_000043.png'
    img_size : int = 640
    batch : int = 30
    server_url : str = 'http://127.0.0.1:8000/api/v1/upload/pil'
    post_mode : str = 'real'
    retry_total : int = 2
    backoff_factor : float = 0.2
    raise_on_status : bool = False
    status_forcelist : tuple = (502, 503, 504)
    pool_connections : int = 100
    pool_maxsize : int = 100
        
    
@dataclass
class Config:
    SERVER: SERVERConfig = field(default_factory=SERVERConfig)


def _get_config_file(config_path : str):
    
    if not os.path.exists(config_path):
        raise ValueError(f"{config_path} is not path")
    
    ext = os.path.splitext(config_path)[1].lower()

    if ext in [".yaml", ".yml"]:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ValueError("YAML root must be a mapping (dict).")
            return data
        
    elif ext == ".py":
        spec = importlib.util.spec_from_file_location("config_module", config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    else:
        raise ValueError(f"Unsupported file type: {ext}")

def _parse_config(config_data : Union[Dict[str, Any], types.ModuleType, Config]) -> Config:
    
    
    if isinstance(config_data, types.ModuleType):
        if hasattr(config_data, "CONFIG") and isinstance(getattr(config_data, "CONFIG"), dict):
            config_data = getattr(config_data, "CONFIG")
        else:
            config_data = {
                "SERVER": getattr(config_data, "SERVER", {}),
            }
            
    if not isinstance(config_data, dict):
        raise TypeError("config_data must be dict/module/Config")
    
    server_raw = _get(config_data, "SERVER", {}) or {}

    server = SERVERConfig(
        content_type=_get(server_raw, "content_type", SERVERConfig.content_type),
        img_path=_get(server_raw, "img_path", SERVERConfig.img_path),
        img_size=int(_get(server_raw, "img_size", SERVERConfig.img_size)),
        batch=int(_get(server_raw, "batch", SERVERConfig.batch)),
        server_url=_get(server_raw, "server_url", SERVERConfig.server_url),
        post_mode=_get(server_raw, "post_mode", SERVERConfig.post_mode),
        retry_total=int(_get(server_raw, "retry_total", SERVERConfig.retry_total)),
        backoff_factor=float(_get(server_raw, "backoff_factor", SERVERConfig.backoff_factor)),
        raise_on_status=bool(_get(server_raw, "raise_on_status", SERVERConfig.raise_on_status)),
        status_forcelist=tuple(_get(server_raw, "status_forcelist", SERVERConfig.status_forcelist)),
        pool_connections=int(_get(server_raw, "pool_connections", SERVERConfig.pool_connections)),
        pool_maxsize=int(_get(server_raw, "pool_maxsize", SERVERConfig.pool_maxsize)),
    )
    
    return Config(
        SERVER=server,
    )
    
def _get(mapping: Dict[str, Any], key: str, default: Any = None) -> Any:
    if not isinstance(mapping, dict):
        return default

    if key in mapping:
        return mapping[key]

    kl = key.lower()
    for k, v in mapping.items():
        if isinstance(k, str) and k.lower() == kl:
            return v
    return default
    
    
def load_config(config_path: str) -> Config:
    raw = _get_config_file(config_path)
    return _parse_config(raw)

def to_yamlable(obj):
    if is_dataclass(obj):
        return {k: to_yamlable(v) for k, v in asdict(obj).items()}

    if isinstance(obj, dict):
        return {to_yamlable(k): to_yamlable(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [to_yamlable(x) for x in obj]

    if isinstance(obj, torch.dtype):
        return str(obj)  # "torch.float32"

    if isinstance(obj, np.ndarray):
        return obj.tolist()
    
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, Enum):
        return obj.value
    return obj

def save_yaml(cfg, path: str):
    data = to_yamlable(cfg)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )

# @dataclass
# class TestConfig():

#     retry_total : int = 2
#     backoff_factor : float = 0.2
#     raise_on_status : bool = False
#     status_forcelist: tuple[int, ...] = (502, 503, 504)
#     pool_connections : int = 100
#     pool_maxsize : int = 100    

#     requests_mod : type = requests
#     img_path : str ='../data/samples/image_000043.png'
#     img_size : int = 640
#     batch : int = 30
#     server_url : str = 'http://127.0.0.1:8000/upload/http_1_1'
#     post_mode: PostMode = PostMode.RAND

#     content_type : ContentType = ContentType.OCTET
    
#     _avail_modes : Set[str] = field(default_factory=lambda: {m.value for m in PostMode}, init=False, repr=False)
#     _avail_ct : Set[str] = field(default_factory=lambda: {m.value for m in ContentType}, init=False, repr=False)

#     def __post_init__(self,):
#         self._check_post_mode()
#         self._check_ct()
                    
        
#     def _check_post_mode(self):
#         if not self.post_mode in self._avail_modes:
#             raise ValueError(f"Only {self._avail_modes} is available!")
        
#     def _check_ct(self):
#         if not self.content_type in self._avail_ct:
#             raise ValueError(f"Only {self._avail_ct} is available!")
        
        
        
def build_session(cfg) -> Session:
    s = Session()
    retry = Retry(
        total=cfg.retry_total,
        backoff_factor=cfg.backoff_factor,
        raise_on_status=cfg.raise_on_status,
        status_forcelist=cfg.status_forcelist,
    )
    adapter = HTTPAdapter(
        pool_connections=cfg.pool_connections,
        pool_maxsize=cfg.pool_maxsize,
        max_retries=retry,
    )
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s
    