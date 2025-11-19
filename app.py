from flask import Flask, request, jsonify
from database import init_db, get_db
import threading
from cleanup_worker import start_cleanup_worker

app = Flask(__name__)
init_db()

@app.get("/tasks")
def list_tasks():
    db = get_db()
    tasks = db.execute("SELECT id, title, done, created_at FROM tasks").fetchall()
    return jsonify([dict(row) for row in tasks])

@app.post("/tasks")
def create_task():
    data = request.json
    title = data.get("title", "")
    db = get_db()
    db.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False))
    db.commit()
    return {"message": "created"}, 201

@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    db.commit()
    return {"message": "updated"}

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return {"message": "deleted"}

threading.Thread(target=start_cleanup_worker, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
