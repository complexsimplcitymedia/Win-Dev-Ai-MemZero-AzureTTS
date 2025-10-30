"""
Configuration Module

Centralized configuration management for Win-Dev-AI.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AzureConfig(BaseModel):
    """Azure Speech Service configuration."""
    subscription_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("AZURE_SPEECH_KEY"),
        description="Azure Speech Service subscription key"
    )
    region: str = Field(
        default_factory=lambda: os.getenv("AZURE_SPEECH_REGION", "eastus"),
        description="Azure region"
    )
    default_voice: str = Field(
        default="en-US-JennyNeural",
        description="Default TTS voice"
    )


class MemoryConfig(BaseModel):
    """Memory management configuration."""
    max_memory_mb: int = Field(
        default=1024,
        description="Maximum memory usage in MB"
    )
    auto_cleanup: bool = Field(
        default=True,
        description="Automatically cleanup on exit"
    )
    encryption_enabled: bool = Field(
        default=True,
        description="Enable memory encryption"
    )


class AIConfig(BaseModel):
    """AI model configuration."""
    openai_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key"
    )
    anthropic_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"),
        description="Anthropic API key"
    )
    default_model: str = Field(
        default="gpt-4",
        description="Default AI model"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Model temperature"
    )
    max_tokens: int = Field(
        default=2000,
        description="Maximum tokens in response"
    )


class AppConfig(BaseModel):
    """Main application configuration."""
    azure: AzureConfig = Field(default_factory=AzureConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    
    enable_voice: bool = Field(
        default=False,
        description="Enable voice output by default"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    class Config:
        """Pydantic config."""
        env_prefix = "WINDEVAI_"


def load_config() -> AppConfig:
    """
    Load application configuration.
    
    Returns:
        AppConfig instance
    """
    return AppConfig()
