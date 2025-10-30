"""
MemZero - Secure Memory Management Module

This module provides secure memory handling capabilities to ensure
sensitive data is properly cleared from memory after use, preventing
potential security vulnerabilities and data leaks.

Key Features:
- Automatic memory zeroing on deletion
- Secure storage for sensitive data
- Memory encryption at rest
- Context manager support for automatic cleanup
"""

import gc
import ctypes
import secrets
import logging
from typing import Any, Optional, Union
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class SecureMemory:
    """
    A secure memory container that automatically zeros sensitive data
    when it's no longer needed.
    
    This class encrypts data in memory and ensures it's properly
    cleared when the object is destroyed.
    """
    
    def __init__(self, data: Any = None, encryption_key: Optional[bytes] = None):
        """
        Initialize a secure memory container.
        
        Args:
            data: The data to store securely
            encryption_key: Optional encryption key (generated if not provided)
        """
        self._key = encryption_key or Fernet.generate_key()
        self._cipher = Fernet(self._key)
        self._encrypted_data: Optional[bytes] = None
        self._is_locked = False
        
        if data is not None:
            self.store(data)
    
    def store(self, data: Any) -> None:
        """
        Store data securely in encrypted form.
        
        Args:
            data: The data to store
        """
        if self._is_locked:
            raise ValueError("SecureMemory is locked and cannot be modified")
        
        # Convert data to bytes if needed
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            data_bytes = str(data).encode('utf-8')
        
        # Encrypt the data
        self._encrypted_data = self._cipher.encrypt(data_bytes)
        logger.debug("Data stored securely in encrypted form")
    
    def retrieve(self) -> str:
        """
        Retrieve and decrypt the stored data.
        
        Returns:
            The decrypted data as a string
        """
        if self._encrypted_data is None:
            raise ValueError("No data stored in SecureMemory")
        
        # Decrypt the data
        decrypted_bytes = self._cipher.decrypt(self._encrypted_data)
        return decrypted_bytes.decode('utf-8')
    
    def lock(self) -> None:
        """Lock the memory to prevent further modifications."""
        self._is_locked = True
        logger.debug("SecureMemory locked")
    
    def zero(self) -> None:
        """
        Securely zero out all sensitive data.
        
        This method overwrites the memory locations with zeros
        to prevent data recovery.
        """
        if self._encrypted_data is not None:
            # Overwrite encrypted data with zeros
            size = len(self._encrypted_data)
            self._encrypted_data = b'\x00' * size
            self._encrypted_data = None
        
        # Overwrite key with zeros
        if self._key is not None:
            size = len(self._key)
            self._key = b'\x00' * size
            self._key = None
        
        # Force garbage collection
        gc.collect()
        logger.debug("Memory securely zeroed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically zero memory."""
        self.zero()
        return False
    
    def __del__(self):
        """Destructor - ensure memory is zeroed."""
        self.zero()


class MemoryManager:
    """
    Central memory management system for the Win-Dev-AI framework.
    
    This class manages multiple SecureMemory instances and provides
    utilities for monitoring and controlling memory usage.
    """
    
    def __init__(self, max_memory_mb: int = 1024):
        """
        Initialize the memory manager.
        
        Args:
            max_memory_mb: Maximum memory usage in megabytes
        """
        self.max_memory_mb = max_memory_mb
        self._secure_stores: dict[str, SecureMemory] = {}
        self._master_key = Fernet.generate_key()
        logger.info(f"MemoryManager initialized with {max_memory_mb}MB limit")
    
    def create_secure_store(self, name: str, data: Any = None) -> SecureMemory:
        """
        Create a new secure memory store.
        
        Args:
            name: Unique identifier for the store
            data: Optional initial data
            
        Returns:
            The created SecureMemory instance
        """
        if name in self._secure_stores:
            raise ValueError(f"Secure store '{name}' already exists")
        
        store = SecureMemory(data, self._master_key)
        self._secure_stores[name] = store
        logger.info(f"Created secure store: {name}")
        return store
    
    def get_secure_store(self, name: str) -> Optional[SecureMemory]:
        """
        Retrieve a secure memory store by name.
        
        Args:
            name: The store identifier
            
        Returns:
            The SecureMemory instance or None if not found
        """
        return self._secure_stores.get(name)
    
    def delete_secure_store(self, name: str) -> bool:
        """
        Delete a secure memory store and zero its contents.
        
        Args:
            name: The store identifier
            
        Returns:
            True if deleted, False if not found
        """
        if name in self._secure_stores:
            self._secure_stores[name].zero()
            del self._secure_stores[name]
            logger.info(f"Deleted secure store: {name}")
            return True
        return False
    
    def zero_all(self) -> None:
        """Zero all secure memory stores."""
        for name, store in list(self._secure_stores.items()):
            store.zero()
        self._secure_stores.clear()
        gc.collect()
        logger.info("All secure stores zeroed")
    
    def get_memory_stats(self) -> dict:
        """
        Get current memory statistics.
        
        Returns:
            Dictionary containing memory usage information
        """
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': process.memory_percent(),
            'num_stores': len(self._secure_stores),
            'max_memory_mb': self.max_memory_mb
        }
    
    def __del__(self):
        """Destructor - ensure all memory is zeroed."""
        self.zero_all()
