from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = "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"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages from Twilio."""
    incoming_message = request.values.get("Body", "").strip()  # User's message
    sender_number = request.values.get("From")  # Sender's phone number
    
    # Log incoming message (for debugging)
    print(f"Incoming message from {sender_number}: {incoming_message}")
    
    # Generate a response using ChatGPT
    gpt_response = generate_chatgpt_response(incoming_message)
    
    # Create Twilio response
    response = MessagingResponse()
    response.message(gpt_response)
    
    return str(response)

def generate_chatgpt_response(user_message):
    """Generate a response from ChatGPT based on the user's message."""
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",  # Use your preferred model (e.g., GPT-3.5-turbo)
            prompt=f"User: {user_message}\nBot:",
            max_tokens=150,
            temperature=0.7
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I'm having trouble understanding you right now. Please try again later."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
