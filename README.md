# Slack Bot with Weather and OpenAI Integration

This repository contains a Python-based Slack bot that fetches weather data from the OpenWeatherMap API and generates responses using OpenAI's GPT models. The bot listens for messages on Slack and replies with weather updates or GPT-enhanced responses.

## Features
- Fetch current weather details for any location using the OpenWeatherMap API.
- Generate natural language responses using OpenAI's GPT models.
- Seamless integration with Slack for message handling and responses.

---

## Prerequisites

### **1. Install Python and Pip**
Make sure you have Python 3.8 or later installed. You can download it from [python.org](https://www.python.org/downloads/).

### **2. Set Up a Slack App**
1. Go to [Slack API Apps](https://api.slack.com/apps) and create a new app.
2. Enable the following permissions under the **OAuth & Permissions** section:
   - `chat:write`
   - `chat:write.public`
   - `commands`
   - `app_mentions:read`
3. Install the app in your workspace and copy the **Bot Token** and **Signing Secret**.

### **3. OpenWeatherMap API**
1. Sign up at [OpenWeatherMap](https://openweathermap.org/) and generate an API key.

### **4. OpenAI API**
1. Create an account at [OpenAI](https://platform.openai.com/) and obtain an API key.

---

## Setup Instructions

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/slack-weather-openai-bot.git
cd slack-weather-openai-bot
```

### **2. Install Dependencies**
Create a virtual environment and install the required packages:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### **3. Create a `.env` File**
Create a `.env` file in the root directory with the following content:

```env
SLACK_TOKEN=your-slack-bot-token
SIGNING_SECRET=your-slack-signing-secret
OPENAI_API_KEY=your-openai-api-key
WEATHER_API_KEY=your-openweathermap-api-key
DEFAULT_LOCATION=your-default-location
```

Replace the placeholders with your actual API keys and desired default location.

### **4. Run the Application**
Start the Flask app to listen for Slack events:
```bash
python app.py
```

The bot will run on `http://localhost:3000`. Make sure to use a tool like [ngrok](https://ngrok.com/) to expose your local server for Slack to send events.

---

## Expose Your Local Server with Ngrok
1. Download and install [ngrok](https://ngrok.com/).
2. Run ngrok to expose your local Flask app:
```bash
ngrok http 3000
```
3. Copy the `https` URL provided by ngrok and paste it into your Slack app's **Event Subscriptions** and **Interactive Components** under the request URL.

---

## Usage
1. Send a message in your Slack workspace mentioning the bot with a location, e.g., `What's the weather in New York?`.
2. The bot will respond with a weather update, enhanced with GPT-generated text.

---

## Troubleshooting
- **Error: Signing secret mismatch**: Ensure your `SIGNING_SECRET` in the `.env` file matches the one in your Slack app.
- **Ngrok not working**: Make sure ngrok is running and the correct URL is entered in your Slack app.
- **OpenWeatherMap API errors**: Check your API key and ensure the location is valid.
- **GPT response errors**: Ensure your OpenAI API key is correct and you have sufficient API credits.

---
