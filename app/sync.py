from garminconnect import Garmin
import os
from dotenv import load_dotenv
from datetime import date
from typing import Any
import json
from pathlib import Path


def sync():
    
    load_dotenv()  # Load variables from .env file
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    print(email)
    print(f"Garmin Connect Progress Tracker for {email}")
    api = Garmin(email, password)
    api.login()

    _today = date.today().strftime('%Y-%m-%d')
    hr_data = api.get_heart_rates(_today)
    print(f"Resting HR: {hr_data.get('restingHeartRate', 'n/a')}")
    
    sync_all(api)
    
def sync_last(api):
    try:
        activities = api.get_activities(
            0, 20
        )  # Get more activities to find a strength training one
        strength_activity = None

        # Find strength training activities
        for activity in activities:
            activity_type = activity.get("activityType", {})
            type_key = activity_type.get("typeKey", "")
            if "strength" in type_key.lower() or "training" in type_key.lower():
                strength_activity = activity
                break
    except Exception as e:
        print("No strength exercises found")
        print(f"Error: {e}")

def sync_last_2_weeks(api):
    pass

def sync_all(api : Garmin):
    activities = api.get_activities(0, 40)
    try:
        for activity in activities:
            activity_type = activity.get("activityType", {})
            type_key = activity_type.get("typeKey", "")
            if "strength" in type_key.lower() or "training" in type_key.lower():
                save_workout_data(activity, api)
    except Exception as e:
        print("No strength exercises found")
        print(f"Error: {e}")
    



def save_workout_data(strength_activity, api):
    try:
        workout_data = api.get_activity_exercise_sets(strength_activity["activityId"])
        save_to_json(strength_activity["activityId"], workout_data)
    except Exception as e:
        print("No strength exercises found")
        print(f"Error: {e}")


def save_to_json(activity_id, data):
    base_dir = Path("../data/jsons")
    base_dir.mkdir(parents=True, exist_ok=True)

    file_path = base_dir / f"{activity_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


