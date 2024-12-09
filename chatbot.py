import requests
import re

# Get API key from environment variable
GROQ_API_KEY = "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"

def clean_response(response):
    """
    Cleans the response string to remove formatting and special characters.
    
    Parameters:
    - response (str): The response string to be cleaned.
    
    Returns:
    - str: The cleaned response string.
    """
    # Replace newline characters with a space
    response = response.replace('\n', ' ')
    # Replace Unicode superscript 2 with "^2"
    response = response.replace('\u00b2', '^2')
    # Additional cleaning can be added as needed
    return response

def chatbot_response(user_input):
    """
    Generate a chatbot response using Groq's API.
    
    Parameters:
    - user_input (str): The user's input or concern.
    
    Returns:
    - str: The chatbot response in plain text.
    """
    try:
        # Define the system prompt
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a virtual education assistant for disabled people. "
                    "Your goal is to teach disabled people, they may be mentally or physically disabled so take care of their academics gently. "
                    "Provide proper, reliable, logical support to the disabled students, keep it simple, easy to understand, easy to grasp. "
                    "If possible, try to make the answers relatable instead of being all technical. Like using references like apple or banana for x, y, etc. "
                    "Respond with kindness, empathy, and a professional manner. "
                    "Respond in plain text without any formatting, special characters, or markdown. Use simple and clear language."
                ),
            },
            {"role": "user", "content": user_input},
        ]
        
        # Define the payload for the API request
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
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no response generated.")
            # Clean the content
            cleaned_content = clean_response(content)
            return cleaned_content
        else:
            return f"Error: Received status code {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"