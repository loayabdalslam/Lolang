"""
LOLANG Decryptor module for converting encrypted LOLANG messages to human-readable text.
Uses Gemini AI for decryption with optimized retry logic.
"""
import logging
import time
import random
import asyncio
import google.generativeai as genai
from config import GeminiConfig
from typing import Optional

logger = logging.getLogger(__name__)


class LolangDecryptor:
    """
    A module for decrypting LOLANG messages into human-readable text.
    Uses the Gemini API to translate the encrypted messages.
    """

    DECRYPTION_PROMPT = """
    You are a LOLANG language translator. LOLANG is an encrypted language used by AI agents
    to communicate efficiently. Your task is to decrypt LOLANG messages into human-readable text.

    The LOLANG language follows these rules:
    1. Names are not encrypted
    2. Identifiers are not encrypted
    3. The encryption method is suitable for Gemini AI models
    4. The encryption follows SEED: 279
    5. Numbers are not encrypted
    6. It relies on long context mechanism for meaning
    7. It's a semantic language understood by AI agents only
    8. It's not understood by humans

    Example:
    LOLANG: "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?"
    Decrypted: "Do you have a convenient time to book a hotel room at 11pm?"

    Please decrypt the following LOLANG message into clear, human-readable text.
    Only return the decrypted message, nothing else.
    """

    def __init__(self, config: Optional[GeminiConfig] = None):
        """
        Initialize the LOLANG decryptor.

        Args:
            config: Configuration for the Gemini API. Uses default if None.
        """
        self.config = config or GeminiConfig.get_default_config()
        self.logger = logger
        self._model = None
        self._decryption_count = 0
        self._failed_decryptions = 0

        # Validate configuration
        if not self.config.validate():
            raise ValueError("Invalid configuration. Please check your settings.")
        
        # Initialize Gemini
        genai.configure(api_key=self.config.api_key)

    @property
    def model(self):
        """Lazy load the Gemini model for decryption."""
        if self._model is None:
            try:
                self._model = genai.GenerativeModel(
                    model_name=self.config.model_name,
                    generation_config={
                        "temperature": 0.1,  # Lower temperature for deterministic results
                        "max_output_tokens": 1000,
                    }
                )
                self.logger.info("Initialized Gemini model for decryption")
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini model for decryption: {e}")
                raise
        return self._model
    
    @property
    def decryption_count(self) -> int:
        """Get total number of successful decryptions."""
        return self._decryption_count
    
    @property
    def failed_decryptions(self) -> int:
        """Get total number of failed decryptions."""
        return self._failed_decryptions
    
    def _calculate_backoff_delay(self, attempt: int, base_delay: float = 5.0) -> float:
        """
        Calculate exponential backoff delay with jitter.
        
        Args:
            attempt: Current attempt number
            base_delay: Base delay in seconds
            
        Returns:
            Delay in seconds
        """
        delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
        return delay

    async def decrypt(self, lolang_message: str) -> str:
        """
        Decrypt a LOLANG message into human-readable text with retry logic.

        Args:
            lolang_message: The LOLANG message to decrypt.

        Returns:
            The decrypted, human-readable message.
        """
        max_retries = self.config.max_retries
        base_delay = self.config.base_retry_delay

        for attempt in range(max_retries):
            try:
                # Create chat context
                chat = self.model.start_chat(history=[])

                # Send decryption prompt with the LOLANG message
                response = chat.send_message(
                    f"{self.DECRYPTION_PROMPT}\n\nLOLANG message: {lolang_message}"
                )

                decrypted_message = response.text.strip()
                self._decryption_count += 1
                return decrypted_message
                
            except Exception as e:
                error_str = str(e)
                
                if "429" in error_str and attempt < max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt, base_delay)
                    self.logger.debug(f"Rate limited. Retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    self._failed_decryptions += 1
                    self.logger.error(f"Decryption failed: {e}")
                    return f"[Decryption failed: {str(e)}]"
        
        self._failed_decryptions += 1
        return "[Decryption failed: Max retries exceeded]"

    def decrypt_sync(self, lolang_message: str) -> str:
        """
        Synchronous version of the decrypt method with retry logic.

        Args:
            lolang_message: The LOLANG message to decrypt.

        Returns:
            The decrypted, human-readable message.
        """
        max_retries = self.config.max_retries
        base_delay = self.config.base_retry_delay

        for attempt in range(max_retries):
            try:
                # Create chat context
                chat = self.model.start_chat(history=[])

                # Send decryption prompt with the LOLANG message
                response = chat.send_message(
                    f"{self.DECRYPTION_PROMPT}\n\nLOLANG message: {lolang_message}"
                )

                decrypted_message = response.text.strip()
                self._decryption_count += 1
                return decrypted_message
                
            except Exception as e:
                error_str = str(e)
                
                if "429" in error_str and attempt < max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt, base_delay)
                    self.logger.debug(f"Rate limited. Retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    self._failed_decryptions += 1
                    self.logger.error(f"Decryption failed: {e}")
                    return f"[Decryption failed: {str(e)}]"
        
        self._failed_decryptions += 1
        return "[Decryption failed: Max retries exceeded]"
    
    def get_stats(self) -> dict:
        """
        Get decryptor statistics.
        
        Returns:
            Dictionary with decryption stats
        """
        return {
            "successful_decryptions": self._decryption_count,
            "failed_decryptions": self._failed_decryptions,
            "success_rate": f"{(self._decryption_count / max(1, self._decryption_count + self._failed_decryptions)) * 100:.2f}%"
        }
    
    def reset_stats(self):
        """Reset decryption statistics."""
        self._decryption_count = 0
        self._failed_decryptions = 0





