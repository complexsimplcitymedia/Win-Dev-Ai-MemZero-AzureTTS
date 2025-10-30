# Setup script for Azure TTS Voice Assistant secrets (Windows PowerShell)

Write-Host "🔐 Azure TTS Voice Assistant - Secrets Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Check if .env exists
if (Test-Path .env) {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
    $confirm = Read-Host "Overwrite? (y/N)"
    if ($confirm -ne 'y') {
        Write-Host "Exiting..."
        exit 0
    }
}

Write-Host ""
Write-Host "📝 Enter your Azure Speech Service credentials:" -ForegroundColor Green
Write-Host "Get them from: https://portal.azure.com" -ForegroundColor Gray
Write-Host "Steps:" -ForegroundColor Gray
Write-Host "  1. Go to Azure Portal -> Create Speech resource" -ForegroundColor Gray
Write-Host "  2. Copy the KEY from Keys and Endpoint" -ForegroundColor Gray
Write-Host "  3. Copy the REGION (e.g., eastus, westus2)" -ForegroundColor Gray
Write-Host ""

# Prompt for credentials
$speech_key = Read-Host "Azure Speech Key"
$region = Read-Host "Azure Region [eastus]"
if ([string]::IsNullOrEmpty($region)) {
    $region = "eastus"
}

# Validate input
if ([string]::IsNullOrEmpty($speech_key)) {
    Write-Host "❌ Error: Azure Speech Key cannot be empty" -ForegroundColor Red
    exit 1
}

# Create .env file
$env_content = @"
# Azure Speech Service Configuration (NEVER commit this file!)
AZURE_SPEECH_KEY=$speech_key
AZURE_SPEECH_REGION=$region

# Optional voice preferences
VOICE_NAME=en-US-AvaMultilingualNeural
VOICE_RATE=+0%
VOICE_PITCH=+0Hz
"@

Set-Content -Path .env -Value $env_content -Encoding UTF8

Write-Host ""
Write-Host "✅ Secrets configured in .env file" -ForegroundColor Green
Write-Host "⚠️  .env is gitignored - NEVER commit it!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Install dependencies: conda env create -f environment.yaml" -ForegroundColor Gray
Write-Host "2. Activate environment: conda activate voice-assistant" -ForegroundColor Gray
Write-Host "3. Test TTS: python -c `"from azure_tts.engine import AzureTTS; engine = AzureTTS(); engine.speak('Hello world')`"" -ForegroundColor Gray
