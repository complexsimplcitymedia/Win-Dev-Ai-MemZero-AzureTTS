"""
MCP Core - Master Control Program
Single source of truth for all gateways and services.
Governs the universal memory system and AI model interactions.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ServiceConfig:
    """Configuration for a registered service."""
    name: str
    service_type: str
    endpoint: str
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GatewayConfig:
    """Configuration for a gateway."""
    name: str
    gateway_type: str
    target_services: List[str] = field(default_factory=list)
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class ServiceRegistry:
    """Registry for all services managed by MCP."""
    
    def __init__(self):
        self.services: Dict[str, ServiceConfig] = {}
        self._lock = threading.Lock()
    
    def register(self, service: ServiceConfig) -> bool:
        """Register a service with MCP."""
        with self._lock:
            if service.name in self.services:
                logger.warning(f"Service {service.name} already registered. Updating.")
            self.services[service.name] = service
            logger.info(f"Registered service: {service.name} ({service.service_type})")
            return True
    
    def unregister(self, service_name: str) -> bool:
        """Unregister a service from MCP."""
        with self._lock:
            if service_name in self.services:
                del self.services[service_name]
                logger.info(f"Unregistered service: {service_name}")
                return True
            return False
    
    def get_service(self, service_name: str) -> Optional[ServiceConfig]:
        """Get a service configuration."""
        return self.services.get(service_name)
    
    def list_services(self, service_type: Optional[str] = None) -> List[ServiceConfig]:
        """List all services, optionally filtered by type."""
        services = list(self.services.values())
        if service_type:
            services = [s for s in services if s.service_type == service_type]
        return services


class Gateway:
    """Gateway for routing requests to appropriate services."""
    
    def __init__(self, config: GatewayConfig, service_registry: ServiceRegistry):
        self.config = config
        self.service_registry = service_registry
        self._lock = threading.Lock()
    
    def route(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route a request to the appropriate service."""
        with self._lock:
            target_service = request.get("target_service")
            if not target_service:
                return {"error": "No target service specified", "success": False}
            
            service = self.service_registry.get_service(target_service)
            if not service:
                return {"error": f"Service {target_service} not found", "success": False}
            
            if not service.enabled:
                return {"error": f"Service {target_service} is disabled", "success": False}
            
            logger.info(f"Gateway {self.config.name} routing to {target_service}")
            return {
                "success": True,
                "gateway": self.config.name,
                "service": target_service,
                "endpoint": service.endpoint
            }


class MasterControlProgram:
    """
    Master Control Program - Single Source of Truth
    Governs all gateways, services, and the universal memory system.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.service_registry = ServiceRegistry()
        self.gateways: Dict[str, Gateway] = {}
        self._lock = threading.Lock()
        self._running = False
        self.metadata = {
            "version": "1.0.0",
            "architecture": "MCP-first",
            "capabilities": ["universal-memory", "model-agnostic", "gateway-routing"]
        }
        
        logger.info("MCP initialized - Master Control Program online")
    
    def register_gateway(self, config: GatewayConfig) -> bool:
        """Register a gateway with MCP."""
        with self._lock:
            gateway = Gateway(config, self.service_registry)
            self.gateways[config.name] = gateway
            logger.info(f"Registered gateway: {config.name} ({config.gateway_type})")
            return True
    
    def unregister_gateway(self, gateway_name: str) -> bool:
        """Unregister a gateway from MCP."""
        with self._lock:
            if gateway_name in self.gateways:
                del self.gateways[gateway_name]
                logger.info(f"Unregistered gateway: {gateway_name}")
                return True
            return False
    
    def get_gateway(self, gateway_name: str) -> Optional[Gateway]:
        """Get a gateway instance."""
        return self.gateways.get(gateway_name)
    
    def register_service(self, service: ServiceConfig) -> bool:
        """Register a service with the MCP service registry."""
        return self.service_registry.register(service)
    
    def route_request(self, gateway_name: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route a request through a specific gateway."""
        gateway = self.get_gateway(gateway_name)
        if not gateway:
            return {"error": f"Gateway {gateway_name} not found", "success": False}
        
        return gateway.route(request)
    
    def start(self):
        """Start the MCP system."""
        with self._lock:
            if self._running:
                logger.warning("MCP already running")
                return
            
            self._running = True
            logger.info("MCP started - All systems operational")
    
    def stop(self):
        """Stop the MCP system."""
        with self._lock:
            if not self._running:
                logger.warning("MCP not running")
                return
            
            self._running = False
            logger.info("MCP stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of MCP and all registered services."""
        return {
            "running": self._running,
            "metadata": self.metadata,
            "services": len(self.service_registry.services),
            "gateways": len(self.gateways),
            "service_list": [s.name for s in self.service_registry.list_services()],
            "gateway_list": list(self.gateways.keys())
        }
    
    def save_config(self, path: Path):
        """Save MCP configuration to file."""
        config = {
            "metadata": self.metadata,
            "services": [
                {
                    "name": s.name,
                    "service_type": s.service_type,
                    "endpoint": s.endpoint,
                    "enabled": s.enabled,
                    "metadata": s.metadata
                }
                for s in self.service_registry.list_services()
            ],
            "gateways": [
                {
                    "name": g.config.name,
                    "gateway_type": g.config.gateway_type,
                    "target_services": g.config.target_services,
                    "enabled": g.config.enabled,
                    "metadata": g.config.metadata
                }
                for g in self.gateways.values()
            ]
        }
        
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"MCP configuration saved to {path}")
    
    def load_config(self, path: Path):
        """Load MCP configuration from file."""
        with open(path, 'r') as f:
            config = json.load(f)
        
        # Load services
        for service_data in config.get("services", []):
            service = ServiceConfig(**service_data)
            self.register_service(service)
        
        # Load gateways
        for gateway_data in config.get("gateways", []):
            gateway_config = GatewayConfig(**gateway_data)
            self.register_gateway(gateway_config)
        
        logger.info(f"MCP configuration loaded from {path}")
