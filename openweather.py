import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
lat = 50.073658
lon = 14.418540

root_url = "https://api.openweathermap.org/data/2.5/weather?"

url = f"{root_url}lat={lat}&lon={lon}&appid={api_key}"

res = requests.get(url)

if res.status_code == 200:
    data = res.json()

    weather = data["weather"][0]["main"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    print(f"Weather: {weather}")
    print(f"Wind Speed: {wind} m/s")
    print(f"Description: {description}")
else:
    print(f"API error: {res.status_code} - {res.reason}")
    print("Response content:", res.text)