
import atexit
import shutil
import subprocess
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Type

from AEYE.application.AI.registry import llm_register

try:
    from langchain_ollama import ChatOllama
except Exception: # pragma: no cover
    ChatOllama = None # type: ignore

try:
    from langchain_openai import ChatOpenAI
except Exception: 
    ChatOpenAI = None

@llm_register.register("LLaMA2")
class LLaMA2:
    
    def __init__(self, ):
        from langchain_community.chat_models import ChatOllama
        self.llm = ChatOllama(model="llama2", temperature=0.2)
        self.process = subprocess.Popen(["ollama", "serve"])

        
    def get_model(self):
        return self.llm
    
    
@dataclass
class LLMConfig:
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: Optional[int] = None
    # provider specific
    base_url: Optional[str] = None # e.g., for OpenAI-compatible endpoints
    api_key: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)



class _OllamaServer:
    _proc: Optional[subprocess.Popen] = None
    _lock = threading.Lock()


    @classmethod
    def ensure_running(cls) -> None:
        if cls._proc and cls._proc.poll() is None:
            return
        with cls._lock:
            if cls._proc and cls._proc.poll() is None:
                return
            if shutil.which("ollama") is None:
                raise RuntimeError("'ollama' CLI not found. Install Ollama first.")
            # Start once and keep alive
            cls._proc = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            atexit.register(cls.stop)


    @classmethod
    def stop(cls) -> None: # graceful
        if cls._proc and cls._proc.poll() is None:
            try:
                cls._proc.terminate()
            except Exception:
                pass
            cls._proc = None
            
            
class BaseLLM:

    def __init__(self, config: Optional[LLMConfig] = None, **overrides: Any) -> None:
        self.config = self._merge_config(config, overrides)
        self._model = self._build()

    def _merge_config(self, config: Optional[LLMConfig], overrides: Dict[str, Any]) -> LLMConfig:
        base = config or LLMConfig()
        # Create a shallow copy and apply overrides
        cfg = LLMConfig(
            model=overrides.get("model", base.model),
            temperature=overrides.get("temperature", base.temperature),
            max_tokens=overrides.get("max_tokens", base.max_tokens),
            base_url=overrides.get("base_url", base.base_url),
            api_key=overrides.get("api_key", base.api_key),
            extra={**(base.extra or {}), **overrides.get("extra", {})},
        )
        return cfg

    def _build(self): # pragma: no cover
        """Return a LangChain-compatible chat model instance."""
        raise NotImplementedError

    def get_model(self):
        return self._model
    
    
class OllamaLLM(BaseLLM):

    def _build(self):
        if ChatOllama is None:
            raise ImportError("langchain_community is required for ChatOllama")
        _OllamaServer.ensure_running()
        kwargs: Dict[str, Any] = {
        "model": self.config.model or "llama2",
        "temperature": self.config.temperature,
        }
        
        if self.config.base_url:
            kwargs["base_url"] = self.config.base_url
        
        if self.config.max_tokens is not None:
            kwargs["num_predict"] = self.config.max_tokens # ChatOllama parameter name
        kwargs.update(self.config.extra)
        return ChatOllama(**kwargs)    
        
    
@llm_register.register("LLaMA2")
class LLaMA2(OllamaLLM):
    def __init__(self, **overrides: Any) -> None:
        super().__init__(LLMConfig(model="llama2", temperature=0.2), **overrides)


@llm_register.register("Mistral")
class Mistral(OllamaLLM):
    def __init__(self, **overrides: Any) -> None:
        super().__init__(LLMConfig(model="mistral", temperature=0.2), **overrides)


@llm_register.register("Qwen2")
class Qwen2(OllamaLLM):
    def __init__(self, **overrides: Any) -> None:
        super().__init__(LLMConfig(model="qwen2", temperature=0.2), **overrides)


@llm_register.register("Phi3")
class Phi3(OllamaLLM):
    def __init__(self, **overrides: Any) -> None:
        super().__init__(LLMConfig(model="phi3", temperature=0.2), **overrides)


def shutdown_llm():
    _OllamaServer.stop()