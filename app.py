from flask import Flask, jsonify, render_template, request,redirect, url_for
import json, os

app = Flask(__name__)
faces = ["bad","notgood","okay","good","great"]
done = False
def write(index):
    print("in")
    data = []
    try:
        with open("save.json", "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = [0,0,0,0,0]
    data[index] += 1
    with open("save.json", "w") as file:
        json.dump(data, file)
@app.route('/item_clicked', methods=['POST'])
def item_clicked():
    global done
    data = request.get_json()
    name = data.get("name")
    write(faces.index(name))
    done = True
    return jsonify({"status": "error"})
@app.route('/')
def index():
    global done
    if done:
        return render_template("end.html", log=faces)
    return render_template("index.html", log=faces)
@app.route('/get_log', methods=['GET'])
def get_log():
    return jsonify({"log": faces})
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)