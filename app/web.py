import os
import sys
from flask import Flask, render_template, jsonify, request
from pathlib import Path
import json

app = Flask(__name__)

def load_exercises():
    json_path = Path(__file__).parent.parent / "data" / "exercise_json" / "parsed_exercises.json"
    
    if not json_path.exists():
        print(f"ERROR: File not found at {json_path}", file=sys.stderr)
        return {}
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data

@app.route("/")
def index():
    exercises = load_exercises()
    if not exercises:
        return """
        <h1>No exercises found!</h1>
        <p>Click the button to sync from Garmin:</p>
        <button onclick="syncData()">Sync Now</button>
        <script>
        async function syncData() {
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = 'Syncing...';
            try {
                const res = await fetch('/sync', { method: 'POST' });
                const data = await res.json();
                alert(data.message);
                location.reload();
            } catch(e) {
                alert('Error: ' + e);
            }
        }
        </script>
        """, 200
    return render_template("index.html", exercises=exercises)

@app.route("/sync", methods=["POST"])
def sync_data():
    """Trigger sync and parse on demand"""
    try:
        from sync import sync
        from parse import parse
        
        print("Starting sync...", file=sys.stderr)
        sync()
        
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)