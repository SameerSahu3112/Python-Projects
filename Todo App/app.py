from flask import Flask, render_template;
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hda77063@localhost/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

if __name__ == '__main__':
    app.run(debug=True, port=3112)

