from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", 
    database="PYPROJECT"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks ORDER BY deadline")
    tasks = cursor.fetchall()
    today = date.today()
    for t in tasks:
        if t['status'].lower() != 'completed':
            if t['deadline'] and t['deadline'] < today:
                t['remark'] = "Overdue"
            elif t['deadline'] == today:
                t['remark'] = "Due Today"
            else:
                t['remark'] = ""
        else:
            t['remark'] = "Done"
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    desc = request.form['description']
    deadline = request.form['deadline']
    priority = request.form['priority']
    cursor.execute("INSERT INTO tasks (title, description, deadline, priority, status) VALUES (%s,%s,%s,%s,%s)",
                   (title, desc, deadline, priority, 'Pending'))
    db.commit()
    return redirect('/')

@app.route('/update/<int:id>')
def update_status(id):
    cursor.execute("UPDATE tasks SET status='Completed' WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
