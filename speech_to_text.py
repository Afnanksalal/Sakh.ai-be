from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the ASR pipeline
try:
    asr_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    logging.info("Speech-to-text pipeline initialized successfully.")
except Exception as e:
    asr_pipe = None
    logging.error(f"Failed to initialize speech-to-text pipeline: {e}", exc_info=True)

def speech_to_text(audio_file):
    """
    Converts speech in an audio file to text using Whisper (small model).
    
    Parameters:
        audio_file (str): Path to the audio file.

    Returns:
        str: Transcribed text or an error message.
    """
    try:
        if asr_pipe is None:
            raise Exception("Speech-to-text pipeline is not initialized.")

        # Perform speech-to-text conversion
        result = asr_pipe(audio_file)

        # Extract and return the transcription
        return result.get("text", "")
    except Exception as e:
        logging.error(f"Error in speech_to_text: {e}", exc_info=True)
        return {"error": str(e)}
