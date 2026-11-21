import os
from flask import Flask, render_template, request, jsonify

# Point Flask to the templates folder in the root directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Temporary in-memory storage (resets when serverless function sleeps)
# Swap this list with database queries (e.g., MySQL/SQLite cloud) for permanent storage
todos = [
    {"id": 1, "task": "Deploy Flask app to Vercel", "done": False}
]
next_id = 2

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def add_todo():
    global next_id
    data = request.get_json()
    task_text = data.get("task", "").strip()
    
    if not task_text:
        return jsonify({"error": "Task cannot be empty"}), 400
        
    new_todo = {"id": next_id, "task": task_text, "done": False}
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201

@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            return jsonify(todo)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"deleted": todo_id})

# Required for local testing (`python api/index.py`)
if __name__ == "__main__":
    app.run(debug=True)