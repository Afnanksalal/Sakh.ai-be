from flask import Flask, request, jsonify, send_file
from summarizer import summarize_text
from text_to_speech import text_to_speech
from speech_to_text import speech_to_text
from chatbot import chatbot_response  # Import the chatbot function
from cbt import cbt_response  # Import the CBT function
from guidance import generate_care_guide  # Import the guidance function
from mentalsupport import mental_support_response  # Import the mental support function
import io
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def alive():
    return jsonify({"status": "alive"}), 200

# Route for text summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    input_text = data.get("input_data", "")
    if not input_text:
        return jsonify({"error": "Input data is required."}), 400
    summary = summarize_text(input_text)
    return jsonify({"output": summary}), 200

# Route for text-to-speech conversion
@app.route('/text_to_speech', methods=['POST'])
def convert_text_to_speech():
    data = request.get_json()
    input_text = data.get("input_data", "")
    accent = data.get("accent", "EN-US")
    speed = data.get("speed", 1.0)
    
    if not input_text:
        return jsonify({"error": "Input data is required."}), 400

    # Convert text to speech
    audio_buffer = text_to_speech(input_text, accent=accent, speed=speed)

    if isinstance(audio_buffer, io.BytesIO):
        return send_file(
            audio_buffer,
            mimetype='audio/wav',
            download_name='output.wav',
            as_attachment=True
        )
    else:
        return jsonify(audio_buffer), 500

# Route for speech-to-text conversion
@app.route('/speech_to_text', methods=['POST'])
def convert_speech_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if file:
        # Save the file temporarily
        temp_path = "/tmp/uploaded_audio.wav"
        file.save(temp_path)

        # Convert speech to text
        transcription = speech_to_text(temp_path)

        # Return transcription or error
        if isinstance(transcription, str):
            return jsonify({"output": transcription}), 200
        else:
            return jsonify(transcription), 500

# Route for chatbot interaction
@app.route('/chatbot', methods=['POST'])
def chatbot():
    """
    Chatbot endpoint to generate responses based on user input.
    Expects JSON payload with 'input_data'.
    """
    data = request.get_json()
    user_input = data.get("input_data", "")
    
    if not user_input:
        return jsonify({"error": "Input data is required."}), 400

    try:
        # Generate chatbot response
        response = chatbot_response(user_input)
        return jsonify({"output": response}), 200
    except Exception as e:
        logging.error(f"Error in chatbot endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate chatbot response."}), 500

# Route for CBT (Cognitive Behavioral Therapy) interaction
@app.route('/cbt', methods=['POST'])
def cbt():
    """
    CBT (Cognitive Behavioral Therapy) endpoint.
    Expects JSON payload with 'input_data'.
    """
    data = request.get_json()
    user_input = data.get("input_data", "")

    if not user_input:
        return jsonify({"error": "Input data is required."}), 400

    try:
        # Generate CBT response
        response = cbt_response(user_input)
        return jsonify({"output": response}), 200
    except Exception as e:
        logging.error(f"Error in CBT endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate CBT response."}), 500

# Route for Guidance (Caregiving guide generation)
@app.route('/guidance', methods=['POST'])
def guidance():
    """
    Guidance endpoint for generating personalized caregiving guide based on user input.
    Expects a POST request with JSON payload containing 'input_data'.
    """
    data = request.get_json()
    user_input = data.get("input_data", "")
    
    if not user_input:
        return jsonify({"error": "Input data is required."}), 400
    
    try:
        # Generate caregiving guide using the user input
        care_guide = generate_care_guide(user_input)
        return jsonify({"output": care_guide}), 200
    except Exception as e:
        logging.error(f"Error in guidance endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate caregiving guide."}), 500

# Route for mental support interaction
@app.route('/mentalsupport', methods=['POST'])
def mentalsupport():
    """
    Mental support endpoint to generate responses based on user input.
    Expects JSON payload with 'input_data'.
    """
    data = request.get_json()
    user_input = data.get("input_data", "")
    
    if not user_input:
        return jsonify({"error": "Input data is required."}), 400

    try:
        # Generate mental support response
        response = mental_support_response(user_input)
        return jsonify({"output": response}), 200
    except Exception as e:
        logging.error(f"Error in mental support endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate mental support response."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)