from melo.api import TTS
import io
from scipy.io.wavfile import read
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Global TTS Model Initialization
device = 'auto'  # Automatically chooses GPU if available
try:
    tts_model = TTS(language='EN', device=device)
    logging.info("TTS Model initialized successfully.")
except Exception as e:
    tts_model = None
    logging.error(f"Failed to initialize TTS Model: {e}", exc_info=True)

def text_to_speech(text, accent='EN-US', speed=1.0):
    try:
        if tts_model is None:
            raise Exception("TTS Model is not initialized.")

        # Map accents to speaker IDs
        speaker_ids = tts_model.hps.data.spk2id
        if accent not in speaker_ids:
            raise ValueError(f"Accent '{accent}' not supported.")

        # Output file for the generated audio
        output_path = 'output.wav'
        
        # Generate speech and save to file
        tts_model.tts_to_file(text, speaker_ids[accent], output_path, speed=speed)
        
        # Read generated audio into BytesIO buffer
        with open(output_path, 'rb') as audio_file:
            buffer = io.BytesIO(audio_file.read())
            buffer.seek(0)
        
        return buffer
    except Exception as e:
        logging.error(f"Error in text_to_speech: {e}", exc_info=True)
        return {"error": str(e)}
