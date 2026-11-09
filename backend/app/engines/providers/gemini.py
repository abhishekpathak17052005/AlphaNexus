import time
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from .base import BaseLLMProvider, LLMResponse


class GeminiProvider(BaseLLMProvider):
    """
    Adapter for Google Gemini API.
    Supports Gemini 1.5 Flash and Gemini 1.5 Pro with structured prompts,
    robust error normalization, and health status reporting.
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            return
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(self.model_name)
            logger.info(f"GeminiProvider initialized with model {self.model_name}")
        except Exception as e:
            logger.warning(f"Failed to configure Gemini client: {e}")
            self._client = None

    def check_availability(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "available": False,
                "provider": "Google Gemini",
                "reason": "GEMINI_API_KEY is not configured",
                "model": self.model_name,
            }
        try:
            # Lightweight probe
            if self._client:
                return {
                    "available": True,
                    "provider": "Google Gemini",
                    "model": self.model_name,
                    "status": "Ready",
                }
            return {
                "available": False,
                "provider": "Google Gemini",
                "reason": "Client initialization failed",
            }
        except Exception as e:
            return {
                "available": False,
                "provider": "Google Gemini",
                "reason": str(e),
            }

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        if not self.api_key or not self._client:
            return LLMResponse(
                content="",
                provider="Google Gemini",
                model=self.model_name,
                tokens_used=0,
                is_live=False,
                error="Gemini provider is not configured (missing GEMINI_API_KEY).",
            )

        start_time = time.time()
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"System Instruction: {system_prompt}\n\nUser Request: {prompt}"

            try:
                response = self._client.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.2, "max_output_tokens": 2048},
                )
                actual_model = self.model_name
            except Exception as initial_err:
                # If model is deprecated or not found (HTTP 404), try supported fallback model
                if "404" in str(initial_err) or "not found" in str(initial_err).lower():
                    logger.warning(
                        f"Configured model '{self.model_name}' unavailable ({initial_err}). "
                        f"Attempting fallback to 'gemini-3.5-flash'."
                    )
                    import google.generativeai as genai
                    fallback_client = genai.GenerativeModel("gemini-3.5-flash")
                    response = fallback_client.generate_content(
                        full_prompt,
                        generation_config={"temperature": 0.2, "max_output_tokens": 2048},
                    )
                    actual_model = "gemini-3.5-flash"
                else:
                    raise initial_err

            text_content = response.text if hasattr(response, "text") else ""
            # Estimate tokens if usage metadata is not directly available
            tokens = 0
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                tokens = getattr(response.usage_metadata, "total_token_count", 0)
            else:
                tokens = len(full_prompt.split()) + len(text_content.split())

            return LLMResponse(
                content=text_content,
                provider="Google Gemini",
                model=actual_model,
                tokens_used=tokens,
                message_type="fact_grounded",
                is_live=True,
            )
        except Exception as e:
            logger.error(f"Gemini API generation error: {e}")
            return LLMResponse(
                content="",
                provider="Google Gemini",
                model=self.model_name,
                is_live=False,
                error=f"Gemini generation error: {str(e)}",
            )

