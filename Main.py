import requests.auth
import datetime
from dotenv import load_dotenv,find_dotenv
import os

# # Get the path for .env file
# # Since we are not literally naming the file ".env", we have to specify the filename:
# # Source: https://stackoverflow.com/questions/41125023/how-to-use-python-dotenvs-find-dotenv-method
env_path = find_dotenv("workout_tracking_variables.env")
print(env_path)
# # load the values from the file:
load_dotenv(env_path)

# # Constant Variables
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

SHEETY_USER = os.getenv("SHEETY_USER")
SHEETY_PASS = os.getenv("SHEETY_PASS")
SHEETY_ID = os.getenv("SHEETY_ID")

GENDER = os.getenv("GENDER")
WEIGHT = os.getenv("WEIGHT")
HEIGHT = os.getenv("HEIGHT")
AGE = os.getenv("AGE")

# # Header for the nutrionix site:
headers_nutri = {"x-app-id": APP_ID,
                 "x-app-key": API_KEY}

nutri_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# # Ask the user for input:
user_text = input("Please input your exercises and their durations :")

# # Parameters - json - data for nutrionix:
nutri_parameters = {"query": user_text,
                    "gender": GENDER,
                    "weight_kg": WEIGHT,
                    "height_cm": HEIGHT,
                    "age": AGE
                    }

# # Note: Dont forget that when we are using the post method, we use data not params.
response = requests.post(url=nutri_endpoint, data=nutri_parameters, headers=headers_nutri)
results = response.json()
print(results)
print(response.status_code)
print(results["exercises"][0])


# # Get todays date-time
todays_hour_now = datetime.datetime.now()
print(todays_hour_now)

# # Format for the date
date = todays_hour_now.strftime("%d/%m/%Y")
# # Format for the hour-min-sec
time = todays_hour_now.strftime("%H:%M:%S")

# # Sheety endpoint:
sheety_endpoint = f"https://api.sheety.co/{SHEETY_ID}/workoutsTracking/workouts"


# # We are going to use a for loop here, in case the user inputs more than 1 type of exercise. So every type of exercise
# # is going to be registered as a seperate key in the dictionary - json response from the server.
for number in results["exercises"]:
    # # Isolate the variables that we need:
    duration_min = number["duration_min"]
    calories = number["nf_calories"]
    exercise = number["name"]
    # # Had an error where no row was getting added. That happend because the parameters were Title cased. For example:
    # # Date instead of date etc...
    # # Source: https://www.udemy.com/course/100-days-of-code/learn/lecture/21311714#questions/13201728

    sheety_parameters = {"workout": {
        "date": date,
        "time": time,
        "exercise": exercise.title(),
        "duration": duration_min,
        "calories": calories,
        "content-Type": "application/json"
    }
                         }
# # Authorization:
    # # Source: https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication
    basic_auth = requests.auth.HTTPBasicAuth(SHEETY_USER,SHEETY_PASS)

    response_2 = requests.post(url=sheety_endpoint, json=sheety_parameters, auth=basic_auth)
    print(response_2.status_code)
    print(response_2.text)
    results_2 = response_2.json()