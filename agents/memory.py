"""
Universal Memory System - Model Agnostic
Frees AI from context limits by providing persistent, searchable memory.
"""

import json
import logging
import hashlib
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """A single memory entry in the universal memory system."""
    id: str
    content: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    importance: float = 1.0
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory entry to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create memory entry from dictionary."""
        return cls(**data)


class UniversalMemory:
    """
    Universal, model-agnostic memory system.
    Stores and manages memories independent of any specific AI model.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("memory/universal_memory.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.memories: Dict[str, MemoryEntry] = {}
        self._lock = threading.Lock()
        self._load_memories()
        
        logger.info(f"Universal Memory initialized with {len(self.memories)} memories")
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID for memory entry."""
        timestamp = str(time.time())
        hash_input = f"{content}{timestamp}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:16]
    
    def _load_memories(self):
        """Load memories from storage."""
        if not self.storage_path.exists():
            logger.info("No existing memory storage found. Starting fresh.")
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.memories = {
                    k: MemoryEntry.from_dict(v) for k, v in data.items()
                }
            logger.info(f"Loaded {len(self.memories)} memories from storage")
        except Exception as e:
            logger.error(f"Error loading memories: {e}")
    
    def _save_memories(self):
        """Save memories to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                data = {k: v.to_dict() for k, v in self.memories.items()}
                json.dump(data, f, indent=2)
            logger.debug(f"Saved {len(self.memories)} memories to storage")
        except Exception as e:
            logger.error(f"Error saving memories: {e}")
    
    def store(self, content: str, metadata: Optional[Dict[str, Any]] = None,
              importance: float = 1.0, tags: Optional[List[str]] = None) -> str:
        """
        Store a new memory entry.
        
        Args:
            content: The content to store
            metadata: Optional metadata dictionary
            importance: Importance score (0.0 to 1.0)
            tags: Optional list of tags
        
        Returns:
            Memory ID
        """
        with self._lock:
            memory_id = self._generate_id(content)
            
            memory = MemoryEntry(
                id=memory_id,
                content=content,
                timestamp=time.time(),
                metadata=metadata or {},
                importance=importance,
                tags=tags or []
            )
            
            self.memories[memory_id] = memory
            self._save_memories()
            
            logger.info(f"Stored memory: {memory_id}")
            return memory_id
    
    def retrieve(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory by ID."""
        with self._lock:
            memory = self.memories.get(memory_id)
            if memory:
                memory.access_count += 1
                memory.last_accessed = time.time()
                self._save_memories()
            return memory
    
    def search(self, query: str, limit: int = 10, 
               min_importance: float = 0.0) -> List[MemoryEntry]:
        """
        Search memories by content.
        Simple text-based search (can be enhanced with embeddings).
        
        Args:
            query: Search query
            limit: Maximum number of results
            min_importance: Minimum importance threshold
        
        Returns:
            List of matching memory entries
        """
        with self._lock:
            query_lower = query.lower()
            matches = []
            
            for memory in self.memories.values():
                if memory.importance < min_importance:
                    continue
                
                # Simple text matching (can be enhanced with semantic search)
                if query_lower in memory.content.lower():
                    matches.append(memory)
            
            # Sort by importance and recency
            matches.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
            
            # Update access statistics
            for memory in matches[:limit]:
                memory.access_count += 1
                memory.last_accessed = time.time()
            
            if matches:
                self._save_memories()
            
            return matches[:limit]
    
    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[MemoryEntry]:
        """Search memories by tags."""
        with self._lock:
            matches = []
            tag_set = set(tags)
            
            for memory in self.memories.values():
                memory_tags = set(memory.tags)
                if tag_set & memory_tags:  # Intersection
                    matches.append(memory)
            
            matches.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
            return matches[:limit]
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory entry."""
        with self._lock:
            if memory_id in self.memories:
                del self.memories[memory_id]
                self._save_memories()
                logger.info(f"Deleted memory: {memory_id}")
                return True
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        with self._lock:
            total_memories = len(self.memories)
            total_accesses = sum(m.access_count for m in self.memories.values())
            avg_importance = (
                sum(m.importance for m in self.memories.values()) / total_memories
                if total_memories > 0 else 0
            )
            
            return {
                "total_memories": total_memories,
                "total_accesses": total_accesses,
                "average_importance": avg_importance,
                "storage_path": str(self.storage_path)
            }
    
    def prune(self, max_age_seconds: Optional[float] = None,
              min_importance: Optional[float] = None,
              max_memories: Optional[int] = None):
        """
        Prune old or low-importance memories.
        
        Args:
            max_age_seconds: Remove memories older than this
            min_importance: Remove memories below this importance
            max_memories: Keep only top N most important memories
        """
        with self._lock:
            current_time = time.time()
            to_remove = []
            
            for memory_id, memory in self.memories.items():
                # Age-based pruning
                if max_age_seconds and (current_time - memory.timestamp) > max_age_seconds:
                    to_remove.append(memory_id)
                    continue
                
                # Importance-based pruning
                if min_importance and memory.importance < min_importance:
                    to_remove.append(memory_id)
                    continue
            
            # Remove marked memories
            for memory_id in to_remove:
                del self.memories[memory_id]
            
            # Size-based pruning
            if max_memories and len(self.memories) > max_memories:
                # Keep top N most important memories
                sorted_memories = sorted(
                    self.memories.items(),
                    key=lambda x: (x[1].importance, x[1].timestamp),
                    reverse=True
                )
                self.memories = dict(sorted_memories[:max_memories])
            
            if to_remove or (max_memories and len(self.memories) > max_memories):
                self._save_memories()
                logger.info(f"Pruned {len(to_remove)} memories")


class MemoryRetriever:
    """
    Advanced memory retrieval system.
    Provides intelligent memory access patterns.
    """
    
    def __init__(self, universal_memory: UniversalMemory):
        self.memory = universal_memory
    
    def get_context(self, query: str, max_tokens: int = 4000) -> str:
        """
        Retrieve relevant context for a query.
        Approximates token count to stay within limits.
        
        Args:
            query: The query to get context for
            max_tokens: Maximum tokens to return (approximated)
        
        Returns:
            Context string assembled from relevant memories
        """
        memories = self.memory.search(query, limit=50)
        
        context_parts = []
        approximate_tokens = 0
        
        for memory in memories:
            # Rough approximation: 4 characters per token
            memory_tokens = len(memory.content) // 4
            
            if approximate_tokens + memory_tokens > max_tokens:
                break
            
            context_parts.append(memory.content)
            approximate_tokens += memory_tokens
        
        context = "\n\n".join(context_parts)
        logger.info(f"Retrieved context: ~{approximate_tokens} tokens from {len(context_parts)} memories")
        
        return context
    
    def get_recent_context(self, limit: int = 10) -> List[MemoryEntry]:
        """Get most recent memories."""
        with self.memory._lock:
            sorted_memories = sorted(
                self.memory.memories.values(),
                key=lambda m: m.timestamp,
                reverse=True
            )
            return sorted_memories[:limit]
    
    def get_important_context(self, limit: int = 10, 
                             min_importance: float = 0.5) -> List[MemoryEntry]:
        """Get most important memories."""
        with self.memory._lock:
            important_memories = [
                m for m in self.memory.memories.values()
                if m.importance >= min_importance
            ]
            important_memories.sort(key=lambda m: m.importance, reverse=True)
            return important_memories[:limit]
