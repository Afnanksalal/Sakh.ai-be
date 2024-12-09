import requests

# Get API key from environment variable
GROQ_API_KEY = "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"
def cbt_response(user_input):
    """
    Generate a CBT response using Groq's API.
    
    Parameters:
    - user_input (str): The user's input or concern.
    
    Returns:
    - str: CBT-based response.
    """
    try:
        # Define the CBT-specific prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a virtual CBT (Cognitive Behavioral Therapy) assistant. "
                    "Your goal is to help users identify and challenge unhelpful thought patterns, "
                    "provide coping mechanisms, and encourage positive thinking. "
                    "Respond with kindness, empathy, and practical CBT techniques."
                ),
            },
            {"role": "user", "content": user_input},
        ]

        # Define the payload for the API
        payload = {
            "model": "llama3-8b-8192",
            "messages": messages,
        }

        # Make the API request
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

        # Parse the response
        if response.status_code == 200:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no response generated.")
        else:
            return f"Error: Received status code {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
