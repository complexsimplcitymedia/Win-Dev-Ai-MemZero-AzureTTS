"""
Memory Service Entry Point
"""
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from src.memory.mem0_client import MemoryClient
    client = MemoryClient()
    client.run()
