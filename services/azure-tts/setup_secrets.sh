#!/bin/bash

# Setup script for Voice Assistant secrets

echo "🔐 Voice Assistant - Secrets Setup"
echo "=================================="

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists"
    read -p "Overwrite? (y/N): " confirm
    if [ "$confirm" != "y" ]; then
        echo "Exiting..."
        exit 0
    fi
fi

# Copy template
cp .env.example .env

echo ""
echo "📝 Enter your Azure Speech Service credentials:"
echo "(Get them from: https://portal.azure.com)"
echo ""

# Prompt for key
read -p "Azure Speech Key: " speech_key
read -p "Azure Region [eastus]: " region
region=${region:-eastus}

# Update .env
sed -i "s/your_key_here/$speech_key/" .env
sed -i "s/eastus/$region/" .env

echo ""
echo "✅ Secrets configured in .env file"
echo "⚠️  .env is gitignored - never commit it!"
echo ""
echo "Test with: conda activate voice-assistant && python voice_assistant.py 'Hello world'"
