"""
WSL-to-Windows TTS Bridge
Enables Azure TTS functionality from WSL Linux environment.
"""

import subprocess
import logging
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureTTSClient:
    """
    Azure Text-to-Speech client.
    Handles communication with Azure Cognitive Services.
    """
    
    def __init__(self, subscription_key: Optional[str] = None, 
                 region: Optional[str] = None):
        self.subscription_key = subscription_key or os.getenv("AZURE_TTS_KEY")
        self.region = region or os.getenv("AZURE_TTS_REGION", "eastus")
        
        if not self.subscription_key:
            logger.warning("Azure TTS subscription key not provided. Set AZURE_TTS_KEY environment variable.")
        
        self.voices = {
            "en-US-JennyNeural": {"gender": "Female", "locale": "en-US"},
            "en-US-GuyNeural": {"gender": "Male", "locale": "en-US"},
            "en-US-AriaNeural": {"gender": "Female", "locale": "en-US"},
            "en-US-DavisNeural": {"gender": "Male", "locale": "en-US"},
            "en-GB-SoniaNeural": {"gender": "Female", "locale": "en-GB"},
            "en-GB-RyanNeural": {"gender": "Male", "locale": "en-GB"},
        }
        
        logger.info(f"Azure TTS Client initialized for region: {self.region}")
    
    def generate_ssml(self, text: str, voice: str = "en-US-JennyNeural",
                     rate: str = "0%", pitch: str = "0%") -> str:
        """
        Generate SSML (Speech Synthesis Markup Language) for Azure TTS.
        
        Args:
            text: Text to convert to speech
            voice: Voice name to use
            rate: Speech rate adjustment (-100% to +200%)
            pitch: Pitch adjustment (-50% to +50%)
        
        Returns:
            SSML formatted string
        """
        ssml = f"""<speak version='1.0' xml:lang='en-US'>
    <voice xml:lang='en-US' name='{voice}'>
        <prosody rate='{rate}' pitch='{pitch}'>
            {text}
        </prosody>
    </voice>
</speak>"""
        return ssml
    
    def list_voices(self) -> Dict[str, Dict[str, str]]:
        """List available voices."""
        return self.voices
    
    def synthesize_speech(self, text: str, output_file: Path,
                         voice: str = "en-US-JennyNeural",
                         rate: str = "0%", pitch: str = "0%") -> bool:
        """
        Synthesize speech from text using Azure TTS.
        This is a placeholder - actual implementation would use Azure SDK.
        
        Args:
            text: Text to synthesize
            output_file: Output audio file path
            voice: Voice to use
            rate: Speech rate
            pitch: Pitch adjustment
        
        Returns:
            True if successful, False otherwise
        """
        if not self.subscription_key:
            logger.error("Cannot synthesize speech: No subscription key provided")
            return False
        
        ssml = self.generate_ssml(text, voice, rate, pitch)
        
        # In a real implementation, this would call Azure Cognitive Services
        logger.info(f"Would synthesize speech to {output_file} using voice {voice}")
        logger.debug(f"SSML: {ssml}")
        
        # Placeholder: Create empty file to indicate where audio would be saved
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(f"Audio placeholder for: {text[:50]}...")
        
        return True


class TTSBridge:
    """
    WSL-to-Windows TTS Bridge.
    Bridges Linux WSL environment to Windows Azure TTS capabilities.
    """
    
    def __init__(self, azure_client: Optional[AzureTTSClient] = None):
        self.azure_client = azure_client or AzureTTSClient()
        self.is_wsl = self._detect_wsl()
        self.windows_path_prefix = "/mnt/c" if self.is_wsl else None
        
        logger.info(f"TTS Bridge initialized (WSL: {self.is_wsl})")
    
    def _detect_wsl(self) -> bool:
        """Detect if running in WSL environment."""
        try:
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                return 'microsoft' in version_info or 'wsl' in version_info
        except FileNotFoundError:
            return False
    
    def _convert_to_windows_path(self, linux_path: Path) -> str:
        """
        Convert WSL Linux path to Windows path.
        
        Args:
            linux_path: Linux path in WSL
        
        Returns:
            Windows path string
        """
        if not self.is_wsl:
            return str(linux_path)
        
        path_str = str(linux_path.absolute())
        
        # Convert /mnt/c/... to C:\...
        if path_str.startswith('/mnt/'):
            drive = path_str[5].upper()
            rest = path_str[6:].replace('/', '\\')
            return f"{drive}:{rest}"
        
        # For paths not in /mnt, use wslpath if available
        try:
            result = subprocess.run(
                ['wslpath', '-w', path_str],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning(f"Could not convert path {path_str} to Windows format")
            return path_str
    
    def _convert_to_linux_path(self, windows_path: str) -> Path:
        """
        Convert Windows path to WSL Linux path.
        
        Args:
            windows_path: Windows path string
        
        Returns:
            Linux path
        """
        if not self.is_wsl:
            return Path(windows_path)
        
        # Convert C:\... to /mnt/c/...
        if ':' in windows_path:
            drive = windows_path[0].lower()
            rest = windows_path[2:].replace('\\', '/')
            return Path(f"/mnt/{drive}{rest}")
        
        return Path(windows_path)
    
    def speak(self, text: str, voice: str = "en-US-JennyNeural",
              output_file: Optional[Path] = None,
              play_audio: bool = True) -> Optional[Path]:
        """
        Convert text to speech using Azure TTS.
        
        Args:
            text: Text to speak
            voice: Voice to use
            output_file: Optional output file path
            play_audio: Whether to play audio immediately (Windows only)
        
        Returns:
            Path to generated audio file
        """
        # Create output file if not provided
        if output_file is None:
            temp_dir = Path(tempfile.gettempdir()) / "tts_bridge"
            temp_dir.mkdir(exist_ok=True)
            output_file = temp_dir / "speech_output.wav"
        
        # Synthesize speech
        success = self.azure_client.synthesize_speech(text, output_file, voice)
        
        if not success:
            logger.error("Speech synthesis failed")
            return None
        
        logger.info(f"Speech synthesized to {output_file}")
        
        # If in WSL and play_audio is requested, try to play on Windows
        if self.is_wsl and play_audio:
            self._play_on_windows(output_file)
        
        return output_file
    
    def _play_on_windows(self, audio_file: Path):
        """
        Play audio file on Windows from WSL.
        
        Args:
            audio_file: Audio file to play
        """
        windows_path = self._convert_to_windows_path(audio_file)
        
        try:
            # Use PowerShell to play audio on Windows
            ps_command = f"(New-Object Media.SoundPlayer '{windows_path}').PlaySync()"
            subprocess.run(
                ['powershell.exe', '-Command', ps_command],
                check=True,
                capture_output=True
            )
            logger.info(f"Played audio on Windows: {windows_path}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not play audio on Windows: {e}")
        except FileNotFoundError:
            logger.warning("PowerShell not found. Audio playback skipped.")
    
    def batch_speak(self, texts: List[str], voice: str = "en-US-JennyNeural",
                   output_dir: Optional[Path] = None) -> List[Path]:
        """
        Convert multiple texts to speech.
        
        Args:
            texts: List of texts to convert
            voice: Voice to use
            output_dir: Output directory for audio files
        
        Returns:
            List of paths to generated audio files
        """
        if output_dir is None:
            output_dir = Path(tempfile.gettempdir()) / "tts_bridge" / "batch"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_files = []
        for i, text in enumerate(texts):
            output_file = output_dir / f"speech_{i:03d}.wav"
            result = self.speak(text, voice, output_file, play_audio=False)
            if result:
                output_files.append(result)
        
        logger.info(f"Batch synthesized {len(output_files)} audio files")
        return output_files
    
    def integrate_with_mcp(self, mcp_instance, service_name: str = "tts_bridge"):
        """
        Integrate TTS Bridge with MCP.
        
        Args:
            mcp_instance: MasterControlProgram instance
            service_name: Service name in MCP
        """
        from mcp.core import ServiceConfig
        
        service = ServiceConfig(
            name=service_name,
            service_type="tts_bridge",
            endpoint="tts://wsl-windows-bridge",
            enabled=True,
            metadata={
                "is_wsl": self.is_wsl,
                "available_voices": list(self.azure_client.voices.keys()),
                "capabilities": ["text-to-speech", "wsl-bridge", "azure-tts"]
            }
        )
        
        mcp_instance.register_service(service)
        logger.info(f"TTS Bridge integrated with MCP as '{service_name}'")
