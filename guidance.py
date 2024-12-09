import requests

# Get API key from environment variable
GROQ_API_KEY = "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"
def generate_care_guide(user_input):
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
                    "You are a virtual Disabality assistant. who helps bystanders to take care of disabled people "
                    "Your goal is to understand what the bystander is going through, what is the disabled person's problems, "
                    "provide proper, reliable, logical support to the bystander to take care of the disabled person based on their disability "
                    "Respond with kindness, empathy, and professional manner."
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
