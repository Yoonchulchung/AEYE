from threading import RLock
from typing import Any

_AEYE_CFG: Any = None
_lock = RLock()

def get_cfg() -> Any:
    global _AEYE_CFG
    
    with _lock:
        if _AEYE_CFG is None:
            raise RuntimeError("cfg has not been set. Call set_cfg(cfg) first.")
        return _AEYE_CFG

def set_cfg(cfg: Any, overwrite: bool = False) -> None:
    global _AEYE_CFG
    with _lock:
        if _AEYE_CFG is not None and not overwrite:
            raise RuntimeError("cfg is already set. Use overwrite=True if you really need to replace it.")
        _AEYE_CFG = cfg