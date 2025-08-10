# app.py
# This is the Python backend script.

from flask import Flask, render_template, request
import requests
import time

# Initialize the Flask app
app = Flask(__name__)

# Your API key from OpenWeatherMap
API_KEY = "ffb398e6eb82b7d53a5a0d6b8b0cb946"

def get_weather_data(city_name, api_key):
    """
    This function fetches real-time weather data from the OpenWeatherMap API.
    It's the same core logic as before, but will be used by our web app.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_details = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature_celsius": data["main"]["temp"],
                "condition": data["weather"][0]["description"].title(),
                "humidity_percent": data["main"]["humidity"],
                "wind_kph": data["wind"]["speed"] * 3.6, # Convert m/s to km/h
                "feels_like_celsius": data["main"]["feels_like"],
                "icon": data["weather"][0]["icon"],
                "error": None
            }
            return weather_details
        else:
            # Return a dictionary with the error message
            error_message = response.json().get("message", "Unknown error")
            return {"error": f"Could not retrieve weather data: {error_message.title()}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"A network error occurred: {e}"}

# Define the main route for the web app
@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    # This block runs when the user submits the form
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather_data(city, API_KEY)
    # This renders the HTML page, passing the weather data to it
    return render_template('index.html', weather=weather)

# This allows you to run the app by executing `python app.py`
if __name__ == '__main__':
    app.run(debug=True)