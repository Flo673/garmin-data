import os
from flask import Flask, render_template, jsonify
from pathlib import Path
import json

app = Flask(__name__)

def load_exercises():
    json_path = Path(__file__).parent.parent / "data" / "exercise_json" / "parsed_exercises.json"
    print(f"Looking for file at: {json_path}")
    print(f"File exists: {json_path.exists()}")
    
    if not json_path.exists():
        print(f"ERROR: File not found at {json_path}")
        return {}
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(f"Loaded {len(data)} exercises")
        return data

@app.route("/")
def index():
    exercises = load_exercises()
    if not exercises:
        return "No exercises found! Check Render logs.", 500
    return render_template("index.html", exercises=exercises)

@app.route("/exercise/<exercise_name>")
def exercise_detail(exercise_name):
    exercises = load_exercises()
    exercise_data = exercises.get(exercise_name, {})
    return render_template("exercise.html", exercise_name=exercise_name, exercise_data=exercise_data)

@app.route("/api/exercises")
def api_exercises():
    return jsonify(load_exercises())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)