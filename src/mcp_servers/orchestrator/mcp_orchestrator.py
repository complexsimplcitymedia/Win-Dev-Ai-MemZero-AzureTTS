"""
MCP Orchestrator - Central hub for all MCP servers
Loads, manages, and coordinates communication between MCP servers
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class MCPOrchestrator:
    """
    Central orchestrator for all MCP servers

    Supported servers:
    - azure_tts: Text-to-Speech (Production)
    - brave: Web search
    - brightdata: Data scraping
    - context7: Documentation
    - duckduckgo: Lightweight search
    - firecrawl: Web scraping
    - github: Repository management
    - nebius: AI inference
    - playwright: Browser automation
    - zapier: Workflow automation
    - job_hunt: Job search aggregator
    """

    AVAILABLE_SERVERS = {
        "azure_tts": {
            "status": "production",
            "description": "Azure Text-to-Speech MCP server",
            "entry_point": "mcp_tts_server.py",
            "priority": 1,
        },
        "brave": {
            "status": "development",
            "description": "Brave Search MCP server",
            "priority": 5,
        },
        "brightdata": {
            "status": "development",
            "description": "Bright Data scraping MCP server",
            "priority": 6,
        },
        "context7": {
            "status": "development",
            "description": "Context7 documentation MCP server",
            "priority": 4,
        },
        "duckduckgo": {
            "status": "development",
            "description": "DuckDuckGo search MCP server",
            "priority": 7,
        },
        "firecrawl": {
            "status": "development",
            "description": "Firecrawl web scraping MCP server",
            "priority": 3,
        },
        "github": {
            "status": "development",
            "description": "GitHub integration MCP server",
            "priority": 8,
        },
        "nebius": {
            "status": "development",
            "description": "Nebius AI inference MCP server",
            "priority": 2,
        },
        "playwright": {
            "status": "development",
            "description": "Playwright browser automation MCP server",
            "priority": 9,
        },
        "zapier": {
            "status": "development",
            "description": "Zapier workflow automation MCP server",
            "priority": 10,
        },
        "job_hunt": {
            "status": "development",
            "description": "Job search aggregator MCP server",
            "priority": 11,
        },
    }

    def __init__(self, mcp_servers_dir: Optional[Path] = None):
        """
        Initialize MCP Orchestrator

        Args:
            mcp_servers_dir: Path to MCP servers directory (default: src/mcp_servers)
        """
        if mcp_servers_dir is None:
            # Assume we're in src/mcp_servers/orchestrator
            mcp_servers_dir = Path(__file__).parent.parent

        self.mcp_servers_dir = Path(mcp_servers_dir)
        self.loaded_servers: Dict[str, Any] = {}
        self.server_configs: Dict[str, Dict] = {}

    async def load_server_configs(self) -> None:
        """Load configuration for all available servers"""
        for server_name, server_info in self.AVAILABLE_SERVERS.items():
            config_path = self.mcp_servers_dir / server_name / "mcp_config_example.json"

            if config_path.exists():
                try:
                    with open(config_path) as f:
                        self.server_configs[server_name] = json.load(f)
                    logger.info(f"Loaded config for {server_name}")
                except Exception as e:
                    logger.warning(f"Failed to load config for {server_name}: {e}")
            else:
                logger.debug(f"No config found for {server_name} at {config_path}")

    async def load_production_servers(self) -> None:
        """Load all production-ready servers"""
        for server_name, info in self.AVAILABLE_SERVERS.items():
            if info["status"] == "production":
                await self._load_server(server_name)

    async def load_all_servers(self) -> None:
        """Load all available servers (including development)"""
        for server_name in sorted(
            self.AVAILABLE_SERVERS.keys(),
            key=lambda x: self.AVAILABLE_SERVERS[x]["priority"],
        ):
            await self._load_server(server_name)

    async def _load_server(self, server_name: str) -> None:
        """
        Load a specific MCP server

        Args:
            server_name: Name of the server to load
        """
        server_info = self.AVAILABLE_SERVERS.get(server_name)
        if not server_info:
            logger.error(f"Unknown server: {server_name}")
            return

        server_dir = self.mcp_servers_dir / server_name
        if not server_dir.exists():
            logger.warning(f"Server directory not found: {server_dir}")
            return

        try:
            logger.info(
                f"Loading {server_name} ({server_info['status']}): {server_info['description']}"
            )
            self.loaded_servers[server_name] = {
                "path": server_dir,
                "info": server_info,
                "config": self.server_configs.get(server_name, {}),
            }
        except Exception as e:
            logger.error(f"Failed to load {server_name}: {e}")

    def get_server_status(self) -> Dict[str, Any]:
        """Get status of all servers"""
        status = {
            "total_available": len(self.AVAILABLE_SERVERS),
            "total_loaded": len(self.loaded_servers),
            "production_servers": sum(
                1
                for info in self.AVAILABLE_SERVERS.values()
                if info["status"] == "production"
            ),
            "development_servers": sum(
                1
                for info in self.AVAILABLE_SERVERS.values()
                if info["status"] == "development"
            ),
            "servers": {},
        }

        for server_name, info in self.AVAILABLE_SERVERS.items():
            status["servers"][server_name] = {
                "status": info["status"],
                "loaded": server_name in self.loaded_servers,
                "priority": info["priority"],
                "description": info["description"],
            }

        return status

    def list_servers(self, status_filter: Optional[str] = None) -> List[str]:
        """
        List available servers

        Args:
            status_filter: Filter by status ('production', 'development', or None for all)

        Returns:
            List of server names
        """
        servers = [
            name
            for name, info in self.AVAILABLE_SERVERS.items()
            if status_filter is None or info["status"] == status_filter
        ]
        return sorted(servers, key=lambda x: self.AVAILABLE_SERVERS[x]["priority"])


# Usage Examples
async def main():
    """Example usage of MCPOrchestrator"""
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    orchestrator = MCPOrchestrator()

    # Load all configurations
    await orchestrator.load_server_configs()

    # Load production servers first
    await orchestrator.load_production_servers()
    print("Production servers loaded:")
    status = orchestrator.get_server_status()
    print(f"  Loaded: {status['total_loaded']}/{status['total_available']}")
    print(f"  Production: {status['production_servers']}")

    # Then load development servers (optional)
    await orchestrator.load_all_servers()
    print("\nAll servers loaded:")
    status = orchestrator.get_server_status()
    print(f"  Loaded: {status['total_loaded']}/{status['total_available']}")

    # List servers by status
    print(
        "\nProduction servers:", orchestrator.list_servers(status_filter="production")
    )
    print(
        "\nDevelopment servers:", orchestrator.list_servers(status_filter="development")
    )

    # Print full status
    print("\nFull status:")
    import pprint

    pprint.pprint(status)


if __name__ == "__main__":
    asyncio.run(main())
