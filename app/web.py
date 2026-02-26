import os
import sys
from flask import Flask, render_template, jsonify, request
from pathlib import Path
import json
import config

app = Flask(__name__)

def load_exercises():
    json_path = Path(__file__).parent.parent / "data" / "parsed_jsons" / "parsed_exercises.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data
    
def load_categories():
    json_path = Path(__file__).parent.parent / "settings" / "muscle_group_list.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["list"]

@app.route("/")
def index():
    exercises = load_exercises()
    categories = load_categories()
    return render_template("index.html", exercises=exercises, categories=categories)

@app.route("/sync-all", methods=["POST"])
def sync_all_data():
    """Trigger sync and parse on demand"""
    try:
        from sync import sync
        from parse import parse
        
        print("Starting sync...", file=sys.stderr)
        sync(all=True)
        
        print("Starting parse...", file=sys.stderr)
        parse()
        
        exercises = load_exercises()
        return jsonify({
            "success": True,
            "message": f"Synced successfully! Loaded {len(exercises)} exercises.",
            "exercise_count": len(exercises)
        })
    except Exception as e:
        print(f"Sync error: {str(e)}", file=sys.stderr)
        return jsonify({
            "success": False,
            "message": f"Sync failed: {str(e)}"
        }), 500
    
@app.route("/sync-last5", methods=["POST"])
def sync_last_5_data():
    """Trigger sync and parse on demand"""
    try:
        from sync import sync
        from parse import parse
        
        print("Starting sync...", file=sys.stderr)
        sync(all=False)
        
        print("Starting parse...", file=sys.stderr)
        parse()
        
        exercises = load_exercises()
        return jsonify({
            "success": True,
            "message": f"Synced successfully! Loaded {len(exercises)} exercises.",
            "exercise_count": len(exercises)
        })
    except Exception as e:
        print(f"Sync error: {str(e)}", file=sys.stderr)
        return jsonify({
            "success": False,
            "message": f"Sync failed: {str(e)}"
        }), 500

@app.route("/exercise/<exercise_name>")
def exercise_detail(exercise_name):
    exercises = load_exercises()
    exercise_data = exercises.get(exercise_name, {})
    return render_template("exercise.html", exercise_name=exercise_name, exercise_data=exercise_data)

@app.route("/api/exercises")
def api_exercises():
    return jsonify(load_exercises())

@app.route("/settings")
def settings():
    settings_dir = Path(__file__).parent.parent / "settings" / "settings.json"
    with open(settings_dir, "r", encoding="utf-8") as f:
        settings = json.load(f)
    return render_template("settings.html", settings = settings)

@app.route("/api/settings", methods=["GET", "POST"])
def api_settings():
    settings_dir = Path(__file__).parent.parent / "settings" / "settings.json"
    if request.method == "GET":
        with open(settings_dir, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    if request.method == "POST":
        data = request.json
        print(data)
        with open(settings_dir, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        from parse import parse
        parse()
        return jsonify({"success": True, "message": "Settings saved"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)