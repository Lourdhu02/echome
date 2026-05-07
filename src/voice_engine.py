import logging
from pathlib import Path
from typing import Optional

import torch
try:
    import whisper
    from TTS.api import TTS
except ImportError:
    whisper = None
    TTS = None

logger = logging.getLogger(__name__)

class VoiceEngine:
    """
    Handles the Voice Clone Engine pillar of ECHOME.
    Includes ASR (Whisper) and TTS (XTTSv2) with speaker cloning.
    """

    def __init__(self, model_dir: Path = Path("models/voice")):
        self.model_dir = model_dir
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.asr_model = None
        self.tts_model = None
        self.speaker_wav = Path("voice/speaker.wav")

    def load_asr(self, model_name: str = "base"):
        """Loads the Whisper ASR model."""
        if whisper is None:
            logger.error("Whisper not installed. ASR unavailable.")
            return
        logger.info(f"Loading ASR model: {model_name}")
        self.asr_model = whisper.load_model(model_name, device=self.device)

    def load_tts(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        """Loads the Coqui TTS model for voice cloning."""
        if TTS is None:
            logger.error("Coqui TTS not installed. TTS unavailable.")
            return
        logger.info(f"Loading TTS model: {model_name}")
        self.tts_model = TTS(model_name).to(self.device)

    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio file to text."""
        if not self.asr_model:
            self.load_asr()
        
        logger.info(f"Transcribing: {audio_path}")
        result = self.asr_model.transcribe(audio_path)
        return result["text"].strip()

    def synthesize(self, text: str, output_path: str, speaker_wav: Optional[str] = None):
        """Synthesizes text to speech using the cloned voice."""
        if not self.tts_model:
            self.load_tts()
            
        ref_wav = speaker_wav or str(self.speaker_wav)
        if not Path(ref_wav).exists():
            logger.warning(f"Speaker reference wav not found at {ref_wav}. Output will be generic.")
            # In a real scenario, we might want to fail or use a default speaker
            
        logger.info(f"Synthesizing voice output to: {output_path}")
        self.tts_model.tts_to_file(
            text=text,
            speaker_wav=ref_wav,
            language="en",
            file_path=output_path
        )

if __name__ == "__main__":
    # Quick sanity check
    logging.basicConfig(level=logging.INFO)
    engine = VoiceEngine()
    print("Voice Engine initialized.")
