from pathlib import Path
import json
from datetime import datetime, timedelta
import config

def parse():
    bodyweight = 70000
    
    rename_dict = get_renamings()
    settings = get_settings()
    weights = simplify_weight_history()
    weights_cache = build_date_to_weight_cache(weights, config.START_DATE, datetime.today().isoformat())
    muscle_groups = load_categories()
    exercises = {}
    base_dir = Path(__file__).parent.parent / "data" / "raw_exercise_jsons"
    print(f"Parsing JSON files in {base_dir}...")
    for file in base_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sset in data["exerciseSets"]:
                if sset["setType"] == "REST":
                    continue


                exercise_name = sset["exercises"][0]["name"]
                date = sset["startTime"][:10]

                if sset["exercises"][0]["name"] is None:
                    exercise_name = sset["exercises"][0]["category"]
                if exercise_name in rename_dict.keys():
                    exercise_name = rename_dict[exercise_name]
                if sset["weight"] is None:
                    sset["weight"] = 0
                if settings["include_bw"] and exercise_name == "PULL_UP":
                    sset["weight"] += weights_cache[date]

                if exercise_name not in exercises:
                    exercises[exercise_name] = {
                        "analytics": {
                            "statistics": {
                                "rep_max": [[0, ""] for _ in range(12)]
                            },
                            "session_metrics": {
                            }

                        },
                        "sessions": {},
                        "muscle_used": muscle_groups.get(exercise_name, ["UNCATEGORIZED"])
                    }
                if date not in exercises[exercise_name]["sessions"].keys():
                    exercises[exercise_name]["sessions"][date] = []
                    exercises[exercise_name]["analytics"]["session_metrics"][date] = {
                        "estimated_1rm": 0,
                        "estimated_5rm": 0,
                    }
                
                
                exercises[exercise_name]["sessions"][date].append({
                    "activityId": data["activityId"],
                    "ssetID": sset["messageIndex"],
                    "reps": sset["repetitionCount"],
                    "weight": sset["weight"],
                    "date": date,
                })

                curr_session_metrics = exercises[exercise_name]["analytics"]["session_metrics"][date]
                estimated_1rm = calculate1rm(sset["weight"], sset["repetitionCount"])
                if estimated_1rm > curr_session_metrics["estimated_1rm"]:
                    curr_session_metrics["estimated_1rm"] = estimated_1rm
                    curr_session_metrics["estimated_5rm"] = calculate5rm(sset["weight"], sset["repetitionCount"])

                rep_max = exercises[exercise_name]["analytics"]["statistics"]["rep_max"]

                if sset["weight"] is not None and sset["weight"] > rep_max[min(11, sset["repetitionCount"] - 1)][0]:
                    
                    rep_max[min(11, sset["repetitionCount"] - 1)] = [sset["weight"], date, sset["repetitionCount"] < 13]
                    for rep in range(min(10, sset["repetitionCount"] - 2), -1, -1):
                        if sset["weight"] > rep_max[rep][0]:
                            rep_max[rep] = [sset["weight"], date, False]
                        else:
                            break
 
    for exercise_name in exercises:
        exercises[exercise_name]["sessions"] = dict(sorted(exercises[exercise_name]["sessions"].items()))
    # Sort exercises my number of sets
    exercises = dict(sorted(exercises.items(), key=lambda x: sum(len(s) for s in x[1]["sessions"].values()), reverse=True))

    output_dir = Path(__file__).parent.parent / "data" / "parsed_jsons"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "parsed_exercises.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exercises, f, indent=2)

def get_weight_history():
    weight_history_path = Path(__file__).parent.parent / "data" / "parsed_jsons" / "weight_history.json"
    with open(weight_history_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_renamings():
    renaming_path = Path(__file__).parent.parent / "settings" / "grouped_exercises.json"
    with open(renaming_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_settings():
    settings_path = Path(__file__).parent.parent / "settings" / "settings.json"
    with open(settings_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate1rm(weight, reps):
    # Using standard bryzki formula:
    return weight * (1.0 / (1.0278 - 0.0278 * reps))

def calculate5rm(weight, reps):
    # Using standard bryzki formula:
    return calculate1rm(weight, reps) * (1.0 - 0.0278 * 4)

def simplify_weight_history():
    weight_history_path = Path(__file__).parent.parent / "data" / "raw_weight_history" / "raw_weight_history.json"
    with open(weight_history_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    # Extract only date and weight
    simplified = {}
    for summary in raw_data.get("dailyWeightSummaries", []):
        date = summary["summaryDate"]
        weight = summary["latestWeight"]["weight"]
        simplified[date] = weight
    
    output_path = Path(__file__).parent.parent / "data" / "parsed_jsons" / "weight_history.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(simplified, f, indent=2)
    
    return simplified

def build_date_to_weight_cache(weight_history: dict, start_date: str, end_date: str) -> dict:
    cache = {}
    
    weigh_ins = sorted(weight_history.items())
    
    current = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    last_weight = weigh_ins[0][1] if len(weigh_ins) > 0 else 0
    weigh_in_idx = 0
    
    while current <= end:
        date_str = current.isoformat()[:10]
        
        while weigh_in_idx < len(weigh_ins) and weigh_ins[weigh_in_idx][0] <= date_str:
            last_weight = weigh_ins[weigh_in_idx][1]
            weigh_in_idx += 1
        
        cache[date_str] = last_weight
        current += timedelta(days=1)
    
    return cache

def load_categories():
    json_path = Path(__file__).parent.parent / "settings" / "exercise_muscle.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data

