import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import requests
from openai import OpenAI

# Load environment variables from a .env file
env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

# Create a Flask app for handling incoming requests
app = Flask(__name__)

# Set up Slack event listener with the secret token for security
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

# Create a Slack client to interact with Slack's API
client = slack.WebClient(token = os.environ['SLACK_TOKEN'])

# Initialize OpenAI with the API key for generating responses
openai = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Fetching the bot's ID from Slack to avoid the bot responding to itself
BOT_ID = client.api_call("auth.test")['user_id']

# Function to fetch weather data from OpenWeatherMap API
def get_weather(location):
    try:
        # Send request to OpenWeatherMap API for weather details
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.environ['WEATHER_API_KEY']}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Check if the response is valid
        data = response.json()  # Parse JSON response
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        # Return weather details in a readable format
        return f"The current weather in {location} is {weather_description} with a temperature of {temperature}°C and humidity of {humidity}%."
    except requests.RequestException as e:
        # Return error if there was an issue with the request
        return f"Error fetching weather data: {str(e)}"

# Function to generate a response using OpenAI GPT model
def generate_response(message):
    try:
        # Generate a natural language response using OpenAI
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message  # Return the response from GPT model
    except Exception as e:
        # Return error if something went wrong with OpenAI API
        return f"Error generating response: {str(e)}"

# Listen for incoming messages on Slack
processed_events = set()  # To track processed events

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    event_id = event.get('client_msg_id')  # Unique ID for each message
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    # Ignore duplicate events
    if event_id in processed_events:
        return
    processed_events.add(event_id)

    # Ignore bot's own messages
    if BOT_ID == user_id:
        return

    # Ignore edited messages
    if event.get('subtype') == 'message_changed':
        return

    # Default location or extract location from text
    location = os.environ['DEFAULT_LOCATION']
    text = text.rstrip('?').strip()
    if "in" in text:
        location = text.split("in")[-1].strip()

    # Fetch weather and generate response
    weather = get_weather(location)
    final_response = generate_response(weather)
    if not final_response or "Error" in final_response:
        final_response = weather or "Sorry, I couldn't fetch the weather right now. Please try again later."

    # Post response to Slack
    client.chat_postMessage(channel=channel_id, text=final_response)


# Run the Flask app to listen for events
if __name__ == "__main__":
    app.run(debug=True, port=3000)
