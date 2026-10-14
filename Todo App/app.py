from flask import Flask, render_template;
from main import view_tasks, create_task, update_task, delete_task


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    tasks = view_tasks()
    return render_template('tasks.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True, port=3112)


