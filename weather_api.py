import os
import requests

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_current_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "lang": "tr",
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code != 200 or "main" not in data:
            return f"Hava durumu alınamadı: {data.get('message', 'Bilinmeyen hata')}"
        
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return (
            f"{city} için hava durumu:
"
            f"- Sıcaklık: {temp}°C
"
            f"- Açıklama: {desc}
"
            f"- Nem: {humidity}%
"
            f"- Rüzgar: {wind} m/s"
        )
    except Exception as e:
        return f"Hata oluştu: {str(e)}"
