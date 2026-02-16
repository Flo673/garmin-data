from garminconnect import Garmin
import os
from dotenv import load_dotenv
from datetime import date
from typing import Any
import json
from pathlib import Path
import config
from parse import get_settings


def sync(all=False):
    
    load_dotenv()  # Load variables from .env file
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    print(f"Garmin Connect Progress Tracker for {email}")
    api = Garmin(email, password)
    api.login()
    sync_weight_history(api)

    if all:
        sync_all(api)
    else:
        sync_last_5(api)
    

    
def sync_last_5(api):
    try:
        activities = api.get_activities(
            0, 5
        )  # Get more activities to find a strength training one
        strength_activity = None

        # Find strength training activities
        for activity in activities:
            print(activity["activityId"])
            activity_type = activity.get("activityType", {})
            type_key = activity_type.get("typeKey", "")
            if "strength" in type_key.lower() or "training" in type_key.lower():
                save_workout_data(activity, api)
    except Exception as e:
        print("No strength exercises found")
        print(f"Error: {e}")


def sync_all(api : Garmin):
    

    activities = api.get_activities(0, 40)
    try:
        for activity in activities:
            activity_type = activity.get("activityType", {})
            type_key = activity_type.get("typeKey", "")
            if config.PERSONAL and activity.get("startTimeLocal", "")[:10] < config.START_DATE:
                continue
            if "strength" in type_key.lower() or "training" in type_key.lower():
                save_workout_data(activity, api)
    except Exception as e:
        print("No strength exercises found")
        print(f"Error: {e}")
    

def sync_weight_history(api : Garmin):
    weight_history = api.get_weigh_ins(config.START_DATE, date.today().isoformat())
    file_path = Path(__file__).parent.parent / "data" / "raw_weight_history" / "raw_weight_history.json"
    with open(file_path, "w", encoding="utf-8") as f:
            json.dump(weight_history, f, indent=2)
    

def save_workout_data(strength_activity, api):
    try:
        workout_data = api.get_activity_exercise_sets(strength_activity["activityId"])
        save_to_json(strength_activity["activityId"], workout_data)
    except Exception as e:
        print("No strength exercises found")
        print(f"Error: {e}")


def save_to_json(activity_id, data):
    try:
        base_dir = Path(__file__).parent.parent / "data" / "raw_exercise_jsons"
        base_dir.mkdir(parents=True, exist_ok=True)

        file_path = base_dir / f"{activity_id}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Error saving workout data for activity {activity_id}: {e}")

