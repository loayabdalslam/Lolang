"""
Configuration module for LOLANG AI Agent System.
Supports environment variables, multiple configurations, and validation.
"""
from dataclasses import dataclass, field
from typing import Optional
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class GeminiConfig:
    """Configuration for Gemini AI model."""
    
    api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    model_name: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    temperature: float = field(default_factory=lambda: float(os.getenv("GEMINI_TEMPERATURE", "0.8")))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("GEMINI_MAX_TOKENS", "8000")))
    message_delay: float = field(default_factory=lambda: float(os.getenv("GEMINI_MESSAGE_DELAY", "5")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("GEMINI_MAX_RETRIES", "10")))
    base_retry_delay: float = field(default_factory=lambda: float(os.getenv("GEMINI_BASE_RETRY_DELAY", "5")))
    
    def validate(self) -> bool:
        """Validate configuration values."""
        if not self.api_key:
            logger.error("GEMINI_API_KEY is required. Set it in .env file or environment.")
            return False
        if not (0.0 <= self.temperature <= 1.0):
            logger.error("Temperature must be between 0.0 and 1.0")
            return False
        if self.max_tokens <= 0:
            logger.error("Max tokens must be greater than 0")
            return False
        if self.message_delay < 0:
            logger.error("Message delay must be non-negative")
            return False
        return True
    
    @classmethod
    def from_env(cls) -> 'GeminiConfig':
        """Create configuration from environment variables."""
        return cls()
    
    @classmethod
    def get_default_config(cls) -> 'GeminiConfig':
        """Create default configuration."""
        return cls()
    
    @classmethod
    def create_test_config(cls, api_key: str) -> 'GeminiConfig':
        """Create configuration for testing with lower resource usage."""
        return cls(
            api_key=api_key,
            temperature=0.5,
            max_tokens=2000,
            message_delay=2.0,
            max_retries=3
        )
    
    @classmethod
    def create_production_config(cls, api_key: str) -> 'GeminiConfig':
        """Create configuration optimized for production use."""
        return cls(
            api_key=api_key,
            model_name="gemini-2.0-flash",
            temperature=0.7,
            max_tokens=8000,
            message_delay=5.0,
            max_retries=10
        )


@dataclass
class ServerConfig:
    """Configuration for WebSocket server."""
    
    host: str = field(default_factory=lambda: os.getenv("LOLANG_SERVER_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("LOLANG_SERVER_PORT", "8765")))
    max_clients: int = field(default_factory=lambda: int(os.getenv("LOLANG_MAX_CLIENTS", "100")))
    ping_interval: int = field(default_factory=lambda: int(os.getenv("LOLANG_PING_INTERVAL", "20")))
    ping_timeout: int = field(default_factory=lambda: int(os.getenv("LOLANG_PING_TIMEOUT", "10")))
    
    @property
    def uri(self) -> str:
        """Get server URI."""
        return f"ws://{self.host}:{self.port}"
    
    @classmethod
    def get_default_config(cls) -> 'ServerConfig':
        """Create default server configuration."""
        return cls()


@dataclass
class ClientConfig:
    """Configuration for WebSocket client."""
    
    server_uri: str = field(default_factory=lambda: os.getenv("LOLANG_SERVER_URI", "ws://localhost:8765"))
    max_conversations: int = field(default_factory=lambda: int(os.getenv("LOLANG_MAX_CONVERSATIONS", "20")))
    auto_reconnect: bool = field(default_factory=lambda: os.getenv("LOLANG_AUTO_RECONNECT", "true").lower() == "true")
    reconnect_delay: float = field(default_factory=lambda: float(os.getenv("LOLANG_RECONNECT_DELAY", "5.0")))
    max_reconnect_attempts: int = field(default_factory=lambda: int(os.getenv("LOLANG_MAX_RECONNECT_ATTEMPTS", "5")))
    
    @classmethod
    def get_default_config(cls) -> 'ClientConfig':
        """Create default client configuration."""
        return cls()