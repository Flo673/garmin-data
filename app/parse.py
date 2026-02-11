def parse():
    from pathlib import Path
    import json

    exercises = {}
    base_dir = Path(__file__).parent.parent / "data" / "jsons"
    print(f"Parsing JSON files in {base_dir}...")
    for file in base_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for set in data["exerciseSets"]:
                if set["setType"] == "REST":
                    continue
                exercise_name = set["exercises"][0]["category"]
                date = set["startTime"][:10]
                if exercise_name not in exercises:
                    exercises[exercise_name] = {}
                if date not in exercises[exercise_name].keys():
                    exercises[exercise_name][date] = []

                exercises[exercise_name][date].append({
                    "activityName": set["exercises"][0]["name"],
                    "activityId": data["activityId"],
                    "setID": set["messageIndex"],
                    "reps": set["repetitionCount"],
                    "weight": set["weight"],
                    "date": date,
                })

    for exercise_name in exercises:
        exercises[exercise_name] = dict(sorted(exercises[exercise_name].items()))

    output_dir = Path(__file__).parent.parent / "data" / "exercise_json"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "parsed_exercises.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exercises, f, indent=2)


            