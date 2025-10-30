"""
TTS Engine using Azure Cognitive Speech Services
"""

import azure.cognitiveservices.speech as speechsdk
from typing import Iterator, Optional
from .config import TTSConfig

class AzureTTS:
    """Azure Text-to-Speech engine"""
    
    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        
        # Initialize Azure Speech
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.config.azure_key,
            region=self.config.azure_region
        )
        
        self.speech_config.speech_synthesis_voice_name = self.config.voice_name
        
        # Audio output
        self.audio_config = speechsdk.audio.AudioOutputConfig(
            use_default_speaker=True
        )
        
        self.synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=self.audio_config
        )
        
        self.is_speaking = False
    
    def speak(self, text: str, wait: bool = True) -> bool:
        """
        Speak text using TTS
        
        Args:
            text: Text to speak
            wait: Wait for speech to complete
            
        Returns:
            True if successful, False otherwise
        """
        if not text.strip():
            return False
        
        ssml = self._build_ssml(text)
        
        self.is_speaking = True
        
        if wait:
            result = self.synthesizer.speak_ssml_async(ssml).get()
            success = self._handle_result(result)
        else:
            self.synthesizer.speak_ssml_async(ssml)
            success = True
        
        self.is_speaking = False
        return success
    
    def speak_stream(self, text_iterator: Iterator[str]) -> None:
        """
        Speak text as it streams in (sentence by sentence)
        
        Args:
            text_iterator: Iterator yielding text chunks
        """
        buffer = ""
        for chunk in text_iterator:
            buffer += chunk
            # Speak at sentence boundaries
            if any(punct in chunk for punct in '.!?\n'):
                sentences = buffer.split('.')
                for sentence in sentences[:-1]:
                    if sentence.strip():
                        self.speak(sentence + '.', wait=True)
                buffer = sentences[-1]
        
        # Speak remaining text
        if buffer.strip():
            self.speak(buffer)
    
    def _build_ssml(self, text: str) -> str:
        """Build SSML markup for text"""
        text_escaped = (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))
        
        return f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name="{self.config.voice_name}">
                <prosody rate="{self.config.voice_rate}" pitch="{self.config.voice_pitch}">
                    {text_escaped}
                </prosody>
            </voice>
        </speak>
        """
    
    def _handle_result(self, result) -> bool:
        """Handle synthesis result"""
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return True
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print(f"✗ Speech synthesis canceled: {cancellation.reason}")
            if cancellation.reason == speechsdk.CancellationReason.Error:
                print(f"Error: {cancellation.error_details}")
            return False
        return False
    
    def stop(self):
        """Stop current speech synthesis"""
        self.is_speaking = False
    
    def set_voice(self, voice_name: str):
        """Change voice on the fly"""
        self.config.voice_name = voice_name
        self.speech_config.speech_synthesis_voice_name = voice_name
    
    def set_rate(self, rate: str):
        """Change speaking rate (e.g., '+10%', '-20%')"""
        self.config.voice_rate = rate
    
    def set_pitch(self, pitch: str):
        """Change pitch (e.g., '+5Hz', '-10Hz')"""
        self.config.voice_pitch = pitch
