"""
Tests for MemZero Module

Testing secure memory management functionality.
"""

import pytest
import gc
from win_dev_ai.memzero import SecureMemory, MemoryManager


class TestSecureMemory:
    """Test SecureMemory class."""
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving data."""
        mem = SecureMemory()
        test_data = "sensitive_information_12345"
        
        mem.store(test_data)
        retrieved = mem.retrieve()
        
        assert retrieved == test_data
    
    def test_context_manager(self):
        """Test context manager zeroes memory."""
        test_data = "secret_data"
        
        with SecureMemory() as mem:
            mem.store(test_data)
            assert mem.retrieve() == test_data
        
        # After context exit, data should be zeroed
        # (we can't easily test this without checking internal state)
        assert mem._encrypted_data is None
    
    def test_lock_prevents_modification(self):
        """Test that locking prevents further modifications."""
        mem = SecureMemory()
        mem.store("initial_data")
        mem.lock()
        
        with pytest.raises(ValueError):
            mem.store("new_data")
    
    def test_zero_clears_data(self):
        """Test that zero() clears all data."""
        mem = SecureMemory()
        mem.store("sensitive_data")
        mem.zero()
        
        assert mem._encrypted_data is None
        assert mem._key is None


class TestMemoryManager:
    """Test MemoryManager class."""
    
    def test_create_secure_store(self):
        """Test creating a secure store."""
        manager = MemoryManager()
        
        store = manager.create_secure_store("test_store", "test_data")
        
        assert store is not None
        assert manager.get_secure_store("test_store") is not None
    
    def test_duplicate_store_name_raises_error(self):
        """Test that duplicate store names raise an error."""
        manager = MemoryManager()
        manager.create_secure_store("duplicate")
        
        with pytest.raises(ValueError):
            manager.create_secure_store("duplicate")
    
    def test_delete_secure_store(self):
        """Test deleting a secure store."""
        manager = MemoryManager()
        manager.create_secure_store("to_delete", "data")
        
        result = manager.delete_secure_store("to_delete")
        
        assert result is True
        assert manager.get_secure_store("to_delete") is None
    
    def test_zero_all(self):
        """Test zeroing all stores."""
        manager = MemoryManager()
        manager.create_secure_store("store1", "data1")
        manager.create_secure_store("store2", "data2")
        
        manager.zero_all()
        
        assert len(manager._secure_stores) == 0
    
    def test_memory_stats(self):
        """Test getting memory statistics."""
        manager = MemoryManager(max_memory_mb=256)
        manager.create_secure_store("stats_test")
        
        stats = manager.get_memory_stats()
        
        assert 'rss_mb' in stats
        assert 'num_stores' in stats
        assert stats['num_stores'] == 1
        assert stats['max_memory_mb'] == 256


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
