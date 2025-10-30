#!/bin/bash
# Start Azure TTS Flask Server

# Activate rocm conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate rocm

# Install dependencies if needed
pip install -q -r requirements_tts.txt 2>/dev/null

# Start server
echo "========================================"
echo "Azure TTS Flask Server Starting..."
echo "========================================"
echo "Listening on: 0.0.0.0:5000"
echo "Accessible at: http://100.110.82.181:5000 (WSL)"
echo "Accessible at: http://100.110.82.180:5000 (Windows)"
echo ""
echo "Usage: POST /speak with JSON: {\"text\": \"your text here\"}"
echo "Health check: GET /health"
echo "========================================"
python azure_tts_server.py
