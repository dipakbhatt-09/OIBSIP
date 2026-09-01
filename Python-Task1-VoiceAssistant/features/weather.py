import os
import requests

def get_weather(command, speak):
    """Get current weather information for a city."""

    # Read API key from environment variables
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")


    # Check API key
    if not weather_api_key:
        speak("Weather API key is not configured.")
        return


    # Extract location from command
    location = command.lower().strip()

    phrases = [
        "what is the weather in",
        "what is the weather of",
        "what's the weather in",
        "what's the weather of",
        "weather in",
        "weather of",
        "weather at",
        "temperature in",
        "temperature of",
        "forecast in",
        "forecast of",
        "weather",
    ]

    for phrase in phrases:
        location = location.replace(
            phrase,
            ""
        ).strip()


    # Check city name
    if not location:
        speak("Please tell me the city name.")
        return


    # OpenWeather API
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": weather_api_key,
        "units": "metric",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )


        # Invalid API key
        if response.status_code == 401:
            speak("The weather API key is invalid.")
            return


        # City not found
        if response.status_code == 404:
            speak(
                f"I could not find weather information "
                f"for {location}."
            )
            return


        # Other API errors
        if response.status_code != 200:
            speak(
                "Sorry, I could not get the weather "
                "information right now."
            )
            return

        data = response.json()

        city = data["name"]
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        speak(
            f"The weather in {city} is {description}. "
            f"The temperature is "
            f"{temperature:.1f} degrees Celsius."
        )

    except requests.RequestException:
        speak(
            "Sorry, I could not connect to the "
            "weather service."
        )

    except Exception as error:
        print("Weather error:", error)
        speak(
            "Something went wrong while getting "
            "the weather."
        )