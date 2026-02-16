def main():
    from sync import sync
    from parse import parse
    
    syncing = False
    parsing = True
    web_server = True

    make_dirs_and_files()

    if syncing:
        sync(True)
    if parsing:
        parse()
    if web_server:
        from web import app
        print("Starting web server at http://localhost:5000")
        print("On your phone (same WiFi), use your PC's local IP, e.g. http://192.168.x.x:5000")
        app.run(host="0.0.0.0", port=5000, debug=True)

def make_dirs_and_files():
    from pathlib import Path
    basedir_1 = Path(__file__).parent.parent / "data" / "raw_exercise_jsons"
    basedir_2 = Path(__file__).parent.parent / "data" / "parsed_jsons"
    basedir_3 = Path(__file__).parent.parent / "data" / "raw_weight_history"
    basedir_1.mkdir(parents=True, exist_ok=True)
    basedir_2.mkdir(parents=True, exist_ok=True)
    exercise_json_path = basedir_2 / "parsed_exercises.json"
    weight_history_path = Path(__file__).parent.parent / "data" / "parsed_jsons" / "weight_history.json"
    raw_weight_history_path = Path(__file__).parent.parent / "data" / "parsed_jsons" / "raw_weight_history.json"


    if not exercise_json_path.exists():
        with open(exercise_json_path, "w", encoding="utf-8") as f:
            f.write("{}")

    if not weight_history_path.exists():
        with open(weight_history_path, "w", encoding="utf-8") as f:
            f.write("{}")

    if not raw_weight_history_path.exists():
        with open(raw_weight_history_path, "w", encoding="utf-8") as f:
            f.write("{}")
    

if __name__ == "__main__":
    main()