
from flask import Flask, request, render_template_string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Report</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74ebd5, #9face6);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 480px;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            text-align: center;
        }

        h1 {
            color: #263c70;
            margin-top: 0;
        }

        .subtitle {
            color: #666;
            margin-bottom: 25px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #5268d9;
        }

        button {
            width: 100%;
            padding: 14px;
            margin-top: 12px;
            border: none;
            border-radius: 10px;
            background: #5268d9;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #354bb5;
        }

        .error {
            margin-top: 20px;
            padding: 12px;
            background: #ffe5e5;
            color: #b00020;
            border-radius: 8px;
        }

        .weather {
            margin-top: 25px;
            padding: 20px;
            background: #f3f6ff;
            border-radius: 15px;
        }

        .city {
            font-size: 23px;
            font-weight: bold;
            color: #263c70;
        }

        .temperature {
            font-size: 48px;
            font-weight: bold;
            color: #5268d9;
            margin: 10px 0;
        }

        .condition {
            font-size: 18px;
            color: #555;
            margin-bottom: 20px;
        }

        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .item {
            background: white;
            padding: 13px 5px;
            border-radius: 10px;
            color: #444;
            font-size: 14px;
        }

        .item strong {
            display: block;
            margin-top: 8px;
            font-size: 17px;
            color: #263c70;
        }

        .footer {
            color: #777;
            font-size: 12px;
            margin-top: 22px;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🌤 Weather Report</h1>
        <p class="subtitle">Check the weather of any city</p>

        <form method="POST">
            <input
                type="text"
                name="city"
                placeholder="Enter city name (e.g. Bengaluru)"
                value="{{ city }}"
                required
            >
            <button type="submit">Get Weather</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if weather %}
            <div class="weather">
                <div class="city">
                    📍 {{ weather.city }}, {{ weather.country }}
                </div>

                <div class="temperature">
                    {{ weather.temperature }}°C
                </div>

                <div class="condition">
                    {{ weather.condition }}
                </div>

                <div class="details">
                    <div class="item">
                        🌡 Feels Like
                        <strong>{{ weather.feels_like }}°C</strong>
                    </div>

                    <div class="item">
                        💧 Humidity
                        <strong>{{ weather.humidity }}%</strong>
                    </div>

                    <div class="item">
                        💨 Wind Speed
                        <strong>{{ weather.wind }} km/h</strong>
                    </div>

                    <div class="item">
                        🌧 Precipitation
                        <strong>{{ weather.rain }} mm</strong>
                    </div>

                    <div class="item">
                        🔺 Today's High
                        <strong>{{ weather.maximum }}°C</strong>
                    </div>

                    <div class="item">
                        🔻 Today's Low
                        <strong>{{ weather.minimum }}°C</strong>
                    </div>
                </div>

                <p class="footer">
                    Local time: {{ weather.time }}
                </p>
            </div>
        {% endif %}

        <p class="footer">
            Weather data provided by Open-Meteo
        </p>
    </div>
</body>
</html>
"""


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "PythonWeatherApp/1.0"}
    )

    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search?"
    params = urllib.parse.urlencode({
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    })

    geo_data = fetch_json(geo_url + params)
    results = geo_data.get("results", [])

    if not results:
        return None

    place = results[0]

    weather_url = "https://api.open-meteo.com/v1/forecast?"
    weather_params = urllib.parse.urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,"
            "weather_code,wind_speed_10m"
        ),
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 1
    })

    data = fetch_json(weather_url + weather_params)
    current = data["current"]
    daily = data["daily"]

    codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Heavy Drizzle",
        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Light Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        80: "Rain Showers",
        81: "Moderate Rain Showers",
        82: "Heavy Rain Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Hail",
        99: "Heavy Thunderstorm with Hail"
    }

    return {
        "city": place["name"],
        "country": place.get("country", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "rain": current["precipitation"],
        "condition": codes.get(
            current["weather_code"], "Unknown Conditions"
        ),
        "maximum": daily["temperature_2m_max"][0],
        "minimum": daily["temperature_2m_min"][0],
        "time": current["time"]
    }


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = ""
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if city:
            try:
                weather = get_weather(city)

                if weather is None:
                    error = "City not found. Please check the spelling."
            except Exception:
                error = (
                    "Unable to fetch weather. "
                    "Check your internet connection and try again."
                )
        else:
            error = "Please enter a city name."

    return render_template_string(
        HTML,
        weather=weather,
        error=error,
        city=city
    )


if __name__ == "__main__":
    app.run(debug=True)
