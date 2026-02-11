def main():
    from sync import sync
    from parse import parse

    syncing = False
    parsing = False
    web_server = True
    if syncing:
        sync(True)
    if parsing:
        parse()
    if web_server:
        from web import app
        print("Starting web server at http://localhost:5000")
        print("On your phone (same WiFi), use your PC's local IP, e.g. http://192.168.x.x:5000")
        app.run(host="0.0.0.0", port=5000, debug=True)



if __name__ == "__main__":
    main()