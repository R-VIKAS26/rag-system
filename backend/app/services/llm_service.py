"""
LLM Service
Interface for large language models (OpenAI, Anthropic, etc.)
"""
import logging
from typing import Optional, List, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    LLM service wrapper for multiple providers
    """
    
    def __init__(self):
        """Initialize LLM service"""
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.client = None
        self.provider = None

        # Try OpenAI (preferred)
        try:
            if settings.OPENAI_API_KEY:
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())
                    self.provider = "openai"
                except Exception:
                    # Fallback to legacy openai package
                    import openai as _openai
                    _openai.api_key = settings.OPENAI_API_KEY.get_secret_value()
                    self.client = _openai
                    self.provider = "openai_legacy"
                logger.info(f"✅ LLM service initialized with OpenAI ({self.model})")
        except Exception as e:
            logger.warning(f"OpenAI initialization failed: {e}")

        # If OpenAI not configured, try Anthropic
        if not self.client and settings.ANTHROPIC_API_KEY:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY.get_secret_value())
                self.provider = "anthropic"
                logger.info("✅ LLM service initialized with Anthropic")
            except Exception as e:
                logger.warning(f"Could not initialize Anthropic client: {e}")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 1.0,
        **kwargs
    ) -> str:
        """
        Generate text using LLM
        """
        if not self.client:
            logger.warning("LLM service not available")
            return "LLM service is not configured"
        
        try:
            # OpenAI (new or legacy) path
            if self.provider in ("openai", "openai_legacy"):
                try:
                    # new OpenAI client uses chat.completions.create
                    response = None
                    if hasattr(self.client, "chat"):
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature,
                            top_p=top_p,
                            max_tokens=self.max_tokens,
                            **kwargs,
                        )
                        answer = response.choices[0].message.content
                    else:
                        # legacy openai package
                        resp = self.client.ChatCompletion.create(
                            model=self.model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=temperature,
                            top_p=top_p,
                            max_tokens=self.max_tokens,
                            **kwargs,
                        )
                        answer = resp.choices[0].message.content

                except Exception as e:
                    logger.error(f"OpenAI generation error: {e}")
                    raise

            elif self.provider == "anthropic":
                try:
                    # Anthropic client expects a prompt string; use a simple completion call
                    resp = self.client.completions.create(
                        model=self.model,
                        prompt=prompt,
                        max_tokens=self.max_tokens,
                        temperature=temperature,
                        **kwargs,
                    )
                    # Anthropic response structure may differ; attempt to extract text
                    answer = getattr(resp, "completion", None) or resp.get("completion") or ""
                except Exception as e:
                    logger.error(f"Anthropic generation error: {e}")
                    raise
            else:
                logger.warning("No LLM provider available for generation")
                return "LLM provider not configured"
            logger.info(f"Generated response using {self.model}")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def generate_with_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        **kwargs
    ):
        """
        Generate text with streaming
        """
        if not self.client:
            raise ValueError("LLM service not initialized")
        
        try:
            with self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=self.max_tokens,
                stream=True,
                **kwargs
            ) as stream:
                for line in stream:
                    if line.choices[0].delta.content:
                        yield line.choices[0].delta.content
                        
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
            raise
    
    def summarize(self, text: str, max_length: int = 500) -> str:
        """
        Summarize text
        """
        prompt = f"""Summarize the following text in {max_length} characters or less:

{text}

Summary:"""
        
        return self.generate(prompt, temperature=0.5)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        """
        prompt = f"""Extract named entities from the following text. Return as JSON with categories like PERSON, ORGANIZATION, LOCATION, etc.

Text: {text}

Entities (JSON):"""
        
        response = self.generate(prompt, temperature=0.0)
        
        # TODO: Parse JSON response
        return {}
    
    def classify_text(self, text: str, categories: List[str]) -> str:
        """
        Classify text into one of the given categories
        """
        categories_str = ", ".join(categories)
        
        prompt = f"""Classify the following text into one of these categories: {categories_str}

Text: {text}

Classification:"""
        
        return self.generate(prompt, temperature=0.0)


_llm_service: Optional[LLMService] = None


def get_llm_service(force_init: bool = False) -> Optional[LLMService]:
    """Return a cached LLMService instance, initializing on first call."""
    global _llm_service
    if _llm_service is None or force_init:
        try:
            _llm_service = LLMService()
        except Exception as e:
            logger.warning(f"Could not initialize LLM service: {e}")
            _llm_service = None
    return _llm_service
