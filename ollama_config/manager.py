"""
Ollama Manager - Single Shared Instance
Manages a single, shared Ollama instance for all AI models.
"""

import logging
import json
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
import subprocess
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaConfig:
    """Configuration for Ollama instance."""
    
    def __init__(self, host: str = "http://localhost:11434",
                 models_dir: Optional[Path] = None,
                 keep_alive: str = "5m"):
        self.host = host
        self.models_dir = models_dir or Path.home() / ".ollama" / "models"
        self.keep_alive = keep_alive
        self.api_base = f"{host}/api"
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "host": self.host,
            "models_dir": str(self.models_dir),
            "keep_alive": self.keep_alive,
            "api_base": self.api_base
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OllamaConfig':
        """Create config from dictionary."""
        return cls(
            host=data.get("host", "http://localhost:11434"),
            models_dir=Path(data["models_dir"]) if "models_dir" in data else None,
            keep_alive=data.get("keep_alive", "5m")
        )


class OllamaManager:
    """
    Manages a single, shared Ollama instance.
    Ensures all AI models use the same Ollama backend.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls, config: Optional[OllamaConfig] = None):
        """Singleton pattern - ensures only one instance."""
        if cls._instance is None:
            cls._instance = super(OllamaManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config: Optional[OllamaConfig] = None):
        if not self._initialized:
            self.config = config or OllamaConfig()
            self._process = None
            self._loaded_models = set()
            OllamaManager._initialized = True
            logger.info("Ollama Manager initialized (singleton instance)")
    
    def is_running(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.config.host}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def start(self) -> bool:
        """
        Start Ollama service.
        Returns True if started successfully or already running.
        """
        if self.is_running():
            logger.info("Ollama is already running")
            return True
        
        try:
            # Try to start Ollama
            logger.info("Starting Ollama service...")
            self._process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            # Wait for service to be ready
            for _ in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.is_running():
                    logger.info("Ollama service started successfully")
                    return True
            
            logger.error("Ollama service failed to start in time")
            return False
            
        except FileNotFoundError:
            logger.error("Ollama executable not found. Please install Ollama.")
            return False
        except Exception as e:
            logger.error(f"Error starting Ollama: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop Ollama service."""
        if self._process:
            self._process.terminate()
            self._process.wait(timeout=10)
            logger.info("Ollama service stopped")
            return True
        return False
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models in Ollama."""
        if not self.is_running():
            logger.warning("Ollama is not running")
            return []
        
        try:
            response = requests.get(f"{self.config.api_base}/tags")
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])
            logger.info(f"Found {len(models)} models in Ollama")
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """
        Pull/download a model.
        
        Args:
            model_name: Name of the model to pull (e.g., "llama2", "mistral")
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_running():
            logger.error("Ollama is not running. Start it first.")
            return False
        
        try:
            logger.info(f"Pulling model: {model_name}")
            response = requests.post(
                f"{self.config.api_base}/pull",
                json={"name": model_name},
                stream=True,
                timeout=600  # 10 minutes timeout for large models
            )
            
            # Stream the pull progress
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    status = data.get("status", "")
                    if status:
                        logger.debug(f"Pull status: {status}")
            
            logger.info(f"Model {model_name} pulled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
    
    def load_model(self, model_name: str) -> bool:
        """
        Load a model into memory.
        
        Args:
            model_name: Name of the model to load
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_running():
            logger.error("Ollama is not running")
            return False
        
        try:
            # Generate with empty prompt to load model
            response = requests.post(
                f"{self.config.api_base}/generate",
                json={
                    "model": model_name,
                    "prompt": "",
                    "keep_alive": self.config.keep_alive
                }
            )
            response.raise_for_status()
            self._loaded_models.add(model_name)
            logger.info(f"Model {model_name} loaded into memory")
            return True
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return False
    
    def generate(self, model_name: str, prompt: str,
                stream: bool = False, **kwargs) -> Optional[str]:
        """
        Generate text using a model.
        
        Args:
            model_name: Name of the model to use
            prompt: Input prompt
            stream: Whether to stream the response
            **kwargs: Additional generation parameters
        
        Returns:
            Generated text or None if error
        """
        if not self.is_running():
            logger.error("Ollama is not running")
            return None
        
        try:
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": stream,
                "keep_alive": self.config.keep_alive,
                **kwargs
            }
            
            response = requests.post(
                f"{self.config.api_base}/generate",
                json=payload,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                # Stream response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        full_response += chunk
                        if data.get("done", False):
                            break
                return full_response
            else:
                # Non-streaming response
                data = response.json()
                return data.get("response", "")
                
        except Exception as e:
            logger.error(f"Error generating with model {model_name}: {e}")
            return None
    
    def chat(self, model_name: str, messages: List[Dict[str, str]],
            stream: bool = False, **kwargs) -> Optional[str]:
        """
        Chat with a model using message history.
        
        Args:
            model_name: Name of the model to use
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response
            **kwargs: Additional parameters
        
        Returns:
            Response text or None if error
        """
        if not self.is_running():
            logger.error("Ollama is not running")
            return None
        
        try:
            payload = {
                "model": model_name,
                "messages": messages,
                "stream": stream,
                "keep_alive": self.config.keep_alive,
                **kwargs
            }
            
            response = requests.post(
                f"{self.config.api_base}/chat",
                json=payload,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        message = data.get("message", {})
                        chunk = message.get("content", "")
                        full_response += chunk
                        if data.get("done", False):
                            break
                return full_response
            else:
                data = response.json()
                message = data.get("message", {})
                return message.get("content", "")
                
        except Exception as e:
            logger.error(f"Error chatting with model {model_name}: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get Ollama instance status."""
        return {
            "running": self.is_running(),
            "host": self.config.host,
            "loaded_models": list(self._loaded_models),
            "available_models": len(self.list_models())
        }
    
    def integrate_with_mcp(self, mcp_instance, service_name: str = "ollama_shared"):
        """
        Integrate Ollama with MCP.
        
        Args:
            mcp_instance: MasterControlProgram instance
            service_name: Service name in MCP
        """
        from mcp.core import ServiceConfig
        
        service = ServiceConfig(
            name=service_name,
            service_type="ollama_instance",
            endpoint=self.config.host,
            enabled=self.is_running(),
            metadata={
                "singleton": True,
                "models": [m.get("name") for m in self.list_models()],
                "capabilities": ["text-generation", "chat", "embeddings"]
            }
        )
        
        mcp_instance.register_service(service)
        logger.info(f"Ollama integrated with MCP as '{service_name}'")
