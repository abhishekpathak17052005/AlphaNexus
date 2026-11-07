from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str
    provider: str
    model: str
    tokens_used: int = 0
    message_type: str = "synthesis"  # fact_grounded, calculated, synthesis
    is_live: bool = True
    error: Optional[str] = None


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        pass

    @abstractmethod
    def check_availability(self) -> Dict[str, Any]:
        pass

