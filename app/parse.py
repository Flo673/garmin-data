def parse():
    from pathlib import Path
    import json

    exercises = {}
    base_dir = Path(__file__).parent.parent / "data" / "jsons"
    print(f"Parsing JSON files in {base_dir}...")
    for file in base_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sset in data["exerciseSets"]:
                if sset["setType"] == "REST":
                    continue
                exercise_name = sset["exercises"][0]["category"]
                date = sset["startTime"][:10]
                if exercise_name not in exercises:
                    exercises[exercise_name] = {
                        "analytics": {
                            "rep_max": [[0, ""]]*10
                        },
                        "sessions": {}
                    }
                if date not in exercises[exercise_name]["sessions"].keys():
                    exercises[exercise_name]["sessions"][date] = []

                exercises[exercise_name]["sessions"][date].append({
                    "activityName": sset["exercises"][0]["name"],
                    "activityId": data["activityId"],
                    "ssetID": sset["messageIndex"],
                    "reps": sset["repetitionCount"],
                    "weight": sset["weight"],
                    "date": date,
                })
                rep_max = exercises[exercise_name]["analytics"]["rep_max"]

                if sset["weight"] is not None and sset["weight"] > rep_max[min(9, sset["repetitionCount"] - 1)][0]:
                    
                    rep_max[min(9, sset["repetitionCount"] - 1)] = [sset["weight"], date, sset["repetitionCount"] < 11]
                    for rep in range(min(8, sset["repetitionCount"] - 2), -1, -1):
                        if sset["weight"] > rep_max[rep][0]:
                            rep_max[rep] = [sset["weight"], date, False]
                        else:
                            break
 
    for exercise_name in exercises:
        exercises[exercise_name] = dict(sorted(exercises[exercise_name].items()))

    output_dir = Path(__file__).parent.parent / "data" / "exercise_json"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "parsed_exercises.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exercises, f, indent=2)


            