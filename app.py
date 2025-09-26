from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import json, os
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = "thatmatt999"  # required for sessions
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
faces = ["great", "good", "okay", "notgood", "bad"]
def write(index):
    data = []
    try:
        with open("save.json", "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        data = [0, 0, 0, 0, 0]
    data[index] += 1
    logging.info(f"Data is: {data}")
    with open("save.json", "w") as file:
        json.dump(data, file)

@app.route('/item_clicked', methods=['POST'])
def item_clicked():
    data = request.get_json()
    name = data.get("name")
    if name in faces:
        write(faces.index(name))
    session['done'] = True  # only for this visitor
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    if session.get('done'):
        session.pop('done', None)
        return render_template("end.html", log=faces)
    return render_template("ask.html", log=faces)

@app.route('/get_log', methods=['GET'])
def get_log():
    return jsonify({"log": faces})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))