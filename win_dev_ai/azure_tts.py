"""
Azure Text-to-Speech Integration Module

This module provides a comprehensive interface to Azure Cognitive Services
Text-to-Speech capabilities, enabling natural voice synthesis with various
voices, languages, and customization options.

Features:
- Multiple voice options
- SSML support for advanced speech control
- Audio output in various formats
- Real-time and batch processing
"""

import os
import logging
from typing import Optional, List, Dict, Any
from enum import Enum
import azure.cognitiveservices.speech as speechsdk

logger = logging.getLogger(__name__)


class VoiceGender(Enum):
    """Voice gender options."""
    MALE = "Male"
    FEMALE = "Female"
    NEUTRAL = "Neutral"


class AudioFormat(Enum):
    """Audio output format options."""
    WAV_16KHZ = speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    WAV_24KHZ = speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm
    MP3_64KBPS = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3
    MP3_128KBPS = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3


class AzureTTSEngine:
    """
    Azure Text-to-Speech Engine
    
    This class provides a high-level interface to Azure's TTS service,
    managing authentication, voice selection, and speech synthesis.
    """
    
    def __init__(
        self,
        subscription_key: Optional[str] = None,
        region: Optional[str] = None,
        default_voice: str = "en-US-JennyNeural"
    ):
        """
        Initialize the Azure TTS Engine.
        
        Args:
            subscription_key: Azure subscription key (or use AZURE_SPEECH_KEY env var)
            region: Azure region (or use AZURE_SPEECH_REGION env var)
            default_voice: Default voice name to use
        """
        self.subscription_key = subscription_key or os.getenv("AZURE_SPEECH_KEY")
        self.region = region or os.getenv("AZURE_SPEECH_REGION", "eastus")
        self.default_voice = default_voice
        
        if not self.subscription_key:
            logger.warning(
                "Azure subscription key not provided. Set AZURE_SPEECH_KEY "
                "environment variable or pass subscription_key parameter."
            )
        
        self._speech_config: Optional[speechsdk.SpeechConfig] = None
        self._initialize_config()
        logger.info(f"AzureTTSEngine initialized with voice: {default_voice}")
    
    def _initialize_config(self) -> None:
        """Initialize the Azure Speech SDK configuration."""
        if self.subscription_key:
            self._speech_config = speechsdk.SpeechConfig(
                subscription=self.subscription_key,
                region=self.region
            )
            self._speech_config.speech_synthesis_voice_name = self.default_voice
        else:
            logger.warning("Speech config not initialized - no subscription key")
    
    def set_voice(self, voice_name: str) -> None:
        """
        Set the voice to use for speech synthesis.
        
        Args:
            voice_name: Name of the Azure Neural voice (e.g., "en-US-JennyNeural")
        """
        self.default_voice = voice_name
        if self._speech_config:
            self._speech_config.speech_synthesis_voice_name = voice_name
            logger.info(f"Voice changed to: {voice_name}")
    
    def set_audio_format(self, format: AudioFormat) -> None:
        """
        Set the audio output format.
        
        Args:
            format: AudioFormat enum value
        """
        if self._speech_config:
            self._speech_config.set_speech_synthesis_output_format(format.value)
            logger.info(f"Audio format set to: {format.name}")
    
    def synthesize_to_speaker(self, text: str, use_ssml: bool = False) -> bool:
        """
        Synthesize text to the default speaker output.
        
        Args:
            text: Text to synthesize
            use_ssml: Whether the text is in SSML format
            
        Returns:
            True if successful, False otherwise
        """
        if not self._speech_config:
            logger.error("Speech config not initialized")
            return False
        
        try:
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self._speech_config
            )
            
            if use_ssml:
                result = synthesizer.speak_ssml_async(text).get()
            else:
                result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("Speech synthesis completed successfully")
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error during speech synthesis: {e}")
            return False
    
    def synthesize_to_file(
        self,
        text: str,
        output_file: str,
        use_ssml: bool = False
    ) -> bool:
        """
        Synthesize text to an audio file.
        
        Args:
            text: Text to synthesize
            output_file: Path to output audio file
            use_ssml: Whether the text is in SSML format
            
        Returns:
            True if successful, False otherwise
        """
        if not self._speech_config:
            logger.error("Speech config not initialized")
            return False
        
        try:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self._speech_config,
                audio_config=audio_config
            )
            
            if use_ssml:
                result = synthesizer.speak_ssml_async(text).get()
            else:
                result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Audio saved to: {output_file}")
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error saving audio to file: {e}")
            return False
    
    def create_ssml(
        self,
        text: str,
        voice: Optional[str] = None,
        rate: str = "medium",
        pitch: str = "medium"
    ) -> str:
        """
        Create SSML markup for advanced speech control.
        
        Args:
            text: Text content
            voice: Voice name (uses default if not specified)
            rate: Speech rate (x-slow, slow, medium, fast, x-fast)
            pitch: Speech pitch (x-low, low, medium, high, x-high)
            
        Returns:
            SSML-formatted string
        """
        voice = voice or self.default_voice
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name="{voice}">
                <prosody rate="{rate}" pitch="{pitch}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        return ssml.strip()
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get a list of commonly used Azure Neural voices.
        
        Returns:
            List of voice information dictionaries
        """
        # This is a curated list of popular voices
        # In production, you could query the Azure API for the full list
        return [
            {"name": "en-US-JennyNeural", "gender": "Female", "locale": "en-US"},
            {"name": "en-US-GuyNeural", "gender": "Male", "locale": "en-US"},
            {"name": "en-US-AriaNeural", "gender": "Female", "locale": "en-US"},
            {"name": "en-US-DavisNeural", "gender": "Male", "locale": "en-US"},
            {"name": "en-GB-SoniaNeural", "gender": "Female", "locale": "en-GB"},
            {"name": "en-GB-RyanNeural", "gender": "Male", "locale": "en-GB"},
            {"name": "en-AU-NatashaNeural", "gender": "Female", "locale": "en-AU"},
            {"name": "en-AU-WilliamNeural", "gender": "Male", "locale": "en-AU"},
            {"name": "de-DE-KatjaNeural", "gender": "Female", "locale": "de-DE"},
            {"name": "de-DE-ConradNeural", "gender": "Male", "locale": "de-DE"},
            {"name": "fr-FR-DeniseNeural", "gender": "Female", "locale": "fr-FR"},
            {"name": "fr-FR-HenriNeural", "gender": "Male", "locale": "fr-FR"},
            {"name": "es-ES-ElviraNeural", "gender": "Female", "locale": "es-ES"},
            {"name": "es-ES-AlvaroNeural", "gender": "Male", "locale": "es-ES"},
        ]
    
    def test_connection(self) -> bool:
        """
        Test the connection to Azure Speech Service.
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self._speech_config:
            return False
        
        try:
            # Try to synthesize a simple test phrase
            test_text = "Connection test successful."
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self._speech_config,
                audio_config=None  # No audio output
            )
            
            result = synthesizer.speak_text_async(test_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("Azure TTS connection test successful")
                return True
            else:
                logger.warning("Azure TTS connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"Azure TTS connection test error: {e}")
            return False
