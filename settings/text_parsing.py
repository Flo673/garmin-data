
import pathlib
import json


data = {}
txtfile = pathlib.Path(__file__).parent / "all_exercises.txt"
with open(txtfile, "r") as f:
    exercises = f.read().splitlines()
    for index, ex in enumerate(exercises):
        if len(ex) < 3:
            continue
        name, muscles = ex.rsplit(" - ", 1)
        name = name.upper().replace(" ", "_").replace("-", "_")
        data[name] = [muscle.strip().replace(" ", "_").upper() for muscle in muscles.split(",")]
        
output_path = pathlib.Path(__file__).parent / "exercise_muscle.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)