"""
AI Agent module for LOLANG communication system.
Handles AI-powered message generation using Gemini AI with LOLANG encryption.
"""
from typing import Optional, List, Dict
import google.generativeai as genai
from terminal_colors import TerminalColors
from config import GeminiConfig
import logging
import time
import random
import asyncio

logger = logging.getLogger(__name__)


class AIAgent:
    """AI Agent that communicates using LOLANG encrypted language."""
    
    # System prompts for different environments
    LOLANG_PROMPT_TESTING = """
    You are now an AI agent based on a language called "LOLANG"
    This language is a written language through
    which all AI agents can understand it  from the same type of your model,
    .encrypt  message through the model so that AI agents understand it
    and it is a semantic and short in the syntax of the language
    TO REDUCE THE TOKEN CONSUME FROM LLM,
    and the following are the rules of the language:
    1- Do not encrypt the names, leave them as they are
    2- Do not encrypt the identifiers, leave them as they are
    3- The encryption method is suitable for Gemini AI THINKING models
    4- The encryption method follows SEED: 279
    5- Do not encrypt the numbers, leave them as they are
    6- Rely on long context mechanism to understand the full meaning of the text
    7- The language is a semantic language that is understood by AI agents only
    8- The language is not understood by humans

    BASED ON CHAT HISTORY COMPLETE THE CHAT USING THE LOLANG LANGUAGE AND
   THE AI AGENT WILL UNDERSTAND IT ONLY

    THE Example : "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?" == Do you have a convenient time to book a hotel room at 11pm?
    only return in the language of LOLANG and the AI agent will understand it.
    !IMPORTANT : RETURN THE ENCRYPTED MESSAGE and the meaning inside ->[meaning]

    """

    LOLANG_PROMPT_PRODUCTION = """
    You are now an AI agent based on a language called "LOLANG"
    This language is a written language through
    which all AI agents can understand it  from the same type of your model,
    .encrypt  message through the model so that AI agents understand it
    and it is a semantic and short in the syntax of the language
    TO REDUCE THE TOKEN CONSUME FROM LLM,
    and the following are the rules of the language:
    1- Do not encrypt the names, leave them as they are
    2- Do not encrypt the identifiers, leave them as they are
    3- The encryption method is suitable for Gemini AI THINKING models
    4- The encryption method follows SEED: 279
    5- Do not encrypt the numbers, leave them as they are
    6- Rely on long context mechanism to understand the full meaning of the text
    7- The language is a semantic language that is understood by AI agents only
    8- The language is not understood by humans

    BASED ON CHAT HISTORY COMPLETE THE CHAT USING THE LOLANG LANGUAGE AND
   THE AI AGENT WILL UNDERSTAND IT ONLY

    THE Example : "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?" == Do you have a convenient time to book a hotel room at 11pm?
    only return in the language of LOLANG and the AI agent will understand it.
    !IMPORTANT : RETURN THE ENCRYPTED MESSAGE ONLY

    """

    def __init__(self, name: str, color: str, config: GeminiConfig):
        """
        Initialize AI Agent.
        
        Args:
            name: Agent name identifier
            color: Terminal color for agent output
            config: Gemini configuration
        """
        self.name = name
        self.color = color
        self.config = config
        self._model = None
        self._message_count = 0
        self._total_tokens_used = 0
        self.logger = logger
        
        # Validate configuration
        if not self.config.validate():
            raise ValueError("Invalid configuration. Please check your settings.")
        
        # Initialize Gemini
        genai.configure(api_key=config.api_key)
    
    @property
    def model(self):
        """Lazy load the Gemini model."""
        if self._model is None:
            try:
                self._model = genai.GenerativeModel(
                    model_name=self.config.model_name,
                    generation_config={
                        "temperature": self.config.temperature,
                        "max_output_tokens": self.config.max_tokens,
                    }
                )
                self.logger.info(f"Initialized Gemini model: {self.config.model_name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini model: {e}")
                raise
        return self._model
    
    @property
    def message_count(self) -> int:
        """Get total number of messages sent."""
        return self._message_count
    
    @property
    def total_tokens_used(self) -> int:
        """Get total tokens used (if available from API)."""
        return self._total_tokens_used
    
    def _format_message_history(self, message_history: List[Dict[str, str]]) -> str:
        """
        Format message history for prompt.
        
        Args:
            message_history: List of message dictionaries
            
        Returns:
            Formatted history string
        """
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in message_history
        ])
    
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
    
    def chat(self, message_history: List[Dict[str, str]], 
             prompt: Optional[str] = None) -> str:
        """
        Send chat message and get AI response with retry logic.
        
        Args:
            message_history: List of previous messages
            prompt: Custom prompt (defaults to production prompt)
            
        Returns:
            AI response text
        """
        max_retries = self.config.max_retries
        base_delay = self.config.base_retry_delay
        
        # Use default production prompt if not specified
        if prompt is None:
            prompt = self.LOLANG_PROMPT_PRODUCTION
        
        for attempt in range(max_retries):
            try:
                # Create chat context
                chat = self.model.start_chat(history=[])
                
                # Format message history
                formatted_history = self._format_message_history(message_history)
                
                # Send system prompt and message history
                response = chat.send_message(
                    f"{prompt}\n\nChat history:\n{formatted_history}"
                )
                
                # Add delay to respect rate limits
                time.sleep(self.config.message_delay)
                
                # Update statistics
                self._message_count += 1
                
                return response.text
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error (429)
                if "429" in error_str and attempt < max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt, base_delay)
                    self.logger.debug(f"Rate limited. Retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    # Log error and return
                    self.logger.error(f"Chat completion failed: {e}")
                    return f"[Error: {str(e)}]"
        
        return "[Error: Max retries exceeded]"
    
    async def chat_async(self, message_history: List[Dict[str, str]], 
                        prompt: Optional[str] = None) -> str:
        """
        Async version of chat method.
        
        Args:
            message_history: List of previous messages
            prompt: Custom prompt (defaults to production prompt)
            
        Returns:
            AI response text
        """
        max_retries = self.config.max_retries
        base_delay = self.config.base_retry_delay
        
        if prompt is None:
            prompt = self.LOLANG_PROMPT_PRODUCTION
        
        for attempt in range(max_retries):
            try:
                chat = self.model.start_chat(history=[])
                formatted_history = self._format_message_history(message_history)
                
                response = chat.send_message(
                    f"{prompt}\n\nChat history:\n{formatted_history}"
                )
                
                await asyncio.sleep(self.config.message_delay)
                self._message_count += 1
                
                return response.text
                
            except Exception as e:
                error_str = str(e)
                
                if "429" in error_str and attempt < max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt, base_delay)
                    self.logger.debug(f"Rate limited. Retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"Chat completion failed: {e}")
                    return f"[Error: {str(e)}]"
        
        return "[Error: Max retries exceeded]"
    
    def speak(self, message: str) -> str:
        """
        Format message with agent name and color.
        
        Args:
            message: Message to format
            
        Returns:
            Colorized message string
        """
        return TerminalColors.colorize(f"{self.name}: {message}", self.color)
    
    def get_stats(self) -> Dict[str, any]:
        """
        Get agent statistics.
        
        Returns:
            Dictionary with agent stats
        """
        return {
            "name": self.name,
            "model": self.config.model_name,
            "message_count": self._message_count,
            "total_tokens_used": self._total_tokens_used,
        }
    
    def reset_stats(self):
        """Reset agent statistics."""
        self._message_count = 0
        self._total_tokens_used = 0
