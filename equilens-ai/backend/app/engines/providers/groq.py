from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from .base import BaseLLMProvider, LLMResponse


class GroqProvider(BaseLLMProvider):
    """
    Adapter for Groq High-Speed LLM Inference.
    Serves as an optional provider and automatic fallback.
    """

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.GROQ_MODEL
        self._client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            return
        try:
            from groq import Groq
            self._client = Groq(api_key=self.api_key)
            logger.info(f"GroqProvider initialized with model {self.model_name}")
        except Exception as e:
            logger.warning(f"Failed to initialize Groq client: {e}")
            self._client = None

    def check_availability(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "available": False,
                "provider": "Groq",
                "reason": "GROQ_API_KEY is not configured",
                "model": self.model_name,
            }
        return {
            "available": True,
            "provider": "Groq",
            "model": self.model_name,
            "status": "Ready",
        }

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        if not self.api_key or not self._client:
            return LLMResponse(
                content="",
                provider="Groq",
                model=self.model_name,
                tokens_used=0,
                is_live=False,
                error="Groq provider is not configured (missing GROQ_API_KEY).",
            )

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            actual_model = self.model_name
            try:
                completion = self._client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=2048,
                )
            except Exception as initial_err:
                if "404" in str(initial_err) or "model_not_found" in str(initial_err).lower():
                    logger.warning(
                        f"Configured Groq model '{self.model_name}' unavailable ({initial_err}). "
                        f"Attempting fallback to 'qwen/qwen3.8-27b'."
                    )
                    actual_model = "qwen/qwen3.8-27b"
                    completion = self._client.chat.completions.create(
                        model=actual_model,
                        messages=messages,
                        temperature=0.2,
                        max_tokens=2048,
                    )
                else:
                    raise initial_err

            text_content = completion.choices[0].message.content or ""
            tokens = completion.usage.total_tokens if completion.usage else 0

            return LLMResponse(
                content=text_content,
                provider="Groq",
                model=actual_model,
                tokens_used=tokens,
                message_type="fact_grounded",
                is_live=True,
            )
        except Exception as e:
            logger.error(f"Groq API generation error: {e}")
            return LLMResponse(
                content="",
                provider="Groq",
                model=self.model_name,
                is_live=False,
                error=f"Groq generation error: {str(e)}",
            )

