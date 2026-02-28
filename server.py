from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/")
def home():
    return "ToDo Backend Running"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    tasks = load_tasks()
    new_task = request.json
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify({"message": "Task added"})

@app.route("/tasks/<int:index>", methods=["PUT"])
def update_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index] = request.json
        save_tasks(tasks)
        return jsonify({"message": "Task updated"})
    return jsonify({"error": "Invalid index"}), 400

@app.route("/tasks/<int:index>", methods=["DELETE"])
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
        return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    app.run()
