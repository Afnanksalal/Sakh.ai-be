import requests
import json

# Your Groq API Key
GROQ_API_KEY = "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"

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Fine-tuned prompt for mental health support
MENTAL_SUPPORT_PROMPT = (
    "You are an empathetic and supportive assistant designed to provide mental health support. "
    "Your role is to listen attentively, provide emotional support, and guide the user toward "
    "a positive mindset without offering medical advice. Respond with kindness, understanding, "
    "and encouragement."
)

def mental_support_response(user_input, model="llama3-8b-8192", temperature=0.7, max_tokens=200):
    """
    Generate a mental health support response using Groq API with a fine-tuned prompt.

    Parameters:
    - user_input (str): The user's input message.
    - model (str): The Groq model to use (default: llama3-8b-8192).
    - temperature (float): Controls randomness in the output (higher = more random).
    - max_tokens (int): Maximum length of the generated response.

    Returns:
    - str: Chatbot response or error message.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    # Construct the conversation prompt
    messages = [
        {"role": "system", "content": MENTAL_SUPPORT_PROMPT},
        {"role": "user", "content": user_input},
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        # Send the request to Groq API
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract the chatbot response
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Groq API: {e}")
        return "Sorry, I encountered an error."
