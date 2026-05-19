from datetime import timezone
import requests
import datetime
import smtplib
import os

LATITUDE = float(os.environ.get("MY_LATITUDE"))
LONGITUDE = float(os.environ.get("MY_LONGITUDE"))
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")


# Step 2: Get ISS position and check if it's nearby
def is_ISS_nearby():
    response = requests.get(url = "http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    longitude = data["iss_position"]["longitude"]
    latitude = data["iss_position"]["latitude"]
    return abs(LATITUDE - latitude) < 5 and abs(LONGITUDE - longitude) < 5


# Step 1: Check to see if it's nighttime i.e sunset <= curr_time
def is_after_sunset():
    parameters = {"lat": LATITUDE, "lng": LONGITUDE, "formatted": 0}

    # Call sunrise/sunset API to get today's sunset
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Convert response from API into datetime object to allow for easy comparison
    sunset_datetime = datetime.datetime.strptime(data["results"]["sunset"], "%Y-%m-%dT%H:%M:%S%z")
    sunrise_datetime = datetime.datetime.strptime(data["results"]["sunrise"], "%Y-%m-%dT%H:%M:%S%z")
    current_time = datetime.datetime.now(timezone.utc)
    print(sunset_datetime < current_time < sunrise_datetime)
    return sunset_datetime <= current_time or sunrise_datetime >= current_time


# Step 3: If both conditions are met, send email signaling to look up
if is_after_sunset() and is_ISS_nearby():
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=EMAIL_ADDRESS, msg="Look Up!\n\nGo outside and look up!\nThe ISS is nearby!")




