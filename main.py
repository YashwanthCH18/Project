import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "9dcb29f6b7b7759a909e08888559b815"
account_sid = "AC58caba6652c9f2e33b47fe4ccaf49336"
auth_token = "5f41552b8b58666242e0a086d4d37edc"

weather_params = {
    "lat": 12.932595,
    "lon": 77.525916,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

rain = False
for hour_date in weather_data["list"]:
    condition_code = hour_date["weather"][0]["id"]
    if int(condition_code) < 700:
        rain = True

if rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body = "It's Going To Rain Today, Bring An Umbrella",
        from_= "+14193301786",
        to = "+919113939238"
    )
    print(message.status)
