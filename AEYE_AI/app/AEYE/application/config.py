
import importlib
import os
import types
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Union

import numpy as np
import torch
import yaml


@dataclass
class LangchainConfig:
    model : str = "Qwen2"
    chunk_size: int = 1000
    chunk_overlap: int = 100
    temperature: int = 0
    prompt: str = None
    retriever_k: int = 4
    retriever_fetch_k: int = 20
    retriever_mult: float = 0.5

@dataclass
class FASTAPIConfig:
    HOST: str = "localhost"
    PORT: int = 8000
    API_PREFIX: str = "/api"
    VIEW_PREFIX: str = "/view"
    WORKERS: int = 1
    RELOAD : bool = False
    LOG_LEVEL : str = "info"

@dataclass
class Vision_AIConfig:
    model : str = "OCTDL"
    network: str = "vgg16"
    pretrained: bool = True
    checkpoint: str = None
    input_size: int = 224
    in_channels: int = 3
    num_classes: int = 7
    criterion : str = "cross_entropy"
    labels : list = None

@dataclass
class HTTPConfig:
    BATCH_THRESHOLD: int = 256
    BATCH_TIMEOUT: float = 1.0
    
    
@dataclass
class Config:
    type: str = "develop"
    FASTAPI: FASTAPIConfig = field(default_factory=FASTAPIConfig)
    Vision_AI: Vision_AIConfig = field(default_factory=Vision_AIConfig)
    HTTP: HTTPConfig = field(default_factory=HTTPConfig)
    langchain: LangchainConfig = field(default_factory=LangchainConfig)
    

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
                "type": getattr(config_data, "type", "develop"),
                "FASTAPI": getattr(config_data, "FASTAPI", {}),
                "Vision_AI": getattr(config_data, "Vision_AI", {}),
                "HTTP": getattr(config_data, "HTTP", {}),
            }
            
    if not isinstance(config_data, dict):
        raise TypeError("config_data must be dict/module/Config")
    
    fastapi_raw = _get(config_data, "FASTAPI", {}) or {}
    vision_ai_raw = _get(config_data, "Vision_AI", {}) or {}
    http_raw    = _get(config_data, "HTTP", {}) or {}
    langchain_raw = _get(config_data, "langchain", {}) or {}

    fastapi = FASTAPIConfig(
        HOST=_get(fastapi_raw, "HOST", FASTAPIConfig.HOST),
        PORT=int(_get(fastapi_raw, "PORT", FASTAPIConfig.PORT)),
        API_PREFIX=_get(fastapi_raw, "API_PREFIX", FASTAPIConfig.API_PREFIX),
        VIEW_PREFIX=_get(fastapi_raw, "VIEW_PREFIX", FASTAPIConfig.VIEW_PREFIX),
        WORKERS=int(_get(fastapi_raw, "WORKERS", FASTAPIConfig.WORKERS)),
        RELOAD=_get(fastapi_raw, "RELOAD", FASTAPIConfig.RELOAD),
        LOG_LEVEL=_get(fastapi_raw, "LOG_LEVEL", FASTAPIConfig.LOG_LEVEL),
    )
    
    vision_ai = Vision_AIConfig(
        model=_get(vision_ai_raw, "model", Vision_AIConfig.model),
        network=_get(vision_ai_raw, "network", Vision_AIConfig.network),
        pretrained=bool(_get(vision_ai_raw, "pretrained", Vision_AIConfig.pretrained)),
        checkpoint=_get(vision_ai_raw, "checkpoint", Vision_AIConfig.checkpoint),
        input_size=int(_get(vision_ai_raw, "input_size", Vision_AIConfig.input_size)),
        in_channels=int(_get(vision_ai_raw, "in_channels", Vision_AIConfig.in_channels)),
        num_classes=int(_get(vision_ai_raw, "num_classes", Vision_AIConfig.num_classes)),
        criterion=_get(vision_ai_raw, "criterion", Vision_AIConfig.criterion),
        labels=list(_get(vision_ai_raw, "labels", Vision_AIConfig.labels)),
    )
    
    http = HTTPConfig(
        BATCH_THRESHOLD=int(_get(http_raw, "BATCH_THRESHOLD", HTTPConfig.BATCH_THRESHOLD)),
        BATCH_TIMEOUT=float(_get(http_raw, "BATCH_TIMEOUT", HTTPConfig.BATCH_TIMEOUT)),
    )
    
    langchain = LangchainConfig(
        model=_get(langchain_raw, "model", LangchainConfig.model),
        chunk_size=int(_get(langchain_raw, "chunk_size", LangchainConfig.chunk_size)),
        chunk_overlap=int(_get(langchain_raw, "chunk_overlap", LangchainConfig.chunk_overlap)),
        temperature=int(_get(langchain_raw, "temperature", LangchainConfig.temperature)),
        prompt=_get(langchain_raw, "prompt", LangchainConfig.prompt),
        retriever_k=int(_get(langchain_raw, "retriever_k", LangchainConfig.retriever_k)),
        retriever_fetch_k=int(_get(langchain_raw, "retriever_fetch_k", LangchainConfig.retriever_fetch_k)),
        retriever_mult=float(_get(langchain_raw, "retriever_mult", LangchainConfig.retriever_mult)),
    )
    
    return Config(
        type=str(_get(config_data, "type", "develop")),
        FASTAPI=fastapi,
        Vision_AI=vision_ai,
        HTTP=http,
        langchain=langchain,
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