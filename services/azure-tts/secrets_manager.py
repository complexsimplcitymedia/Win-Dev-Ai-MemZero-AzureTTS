#!/usr/bin/env python
"""
Secrets management - reads from .env file or system env vars
"""

import os
from pathlib import Path

def load_env_file(env_path='.env'):
    """Load .env file into environment"""
    env_file = Path(env_path)
    if not env_file.exists():
        return False
    
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value.strip()
    return True

def get_credentials():
    """Get Azure credentials from env"""
    # Try to load .env file first
    load_env_file()
    
    key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
    
    if not key:
        print("❌ AZURE_SPEECH_KEY not found in environment")
        print("Create a .env file from .env.example")
        raise ValueError("Missing Azure Speech Key")
    
    return key, region
