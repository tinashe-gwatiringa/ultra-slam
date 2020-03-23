#! /usr/bin/python3

from flask import Flask, render_template, url_for, request, redirect, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import base64
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():

    img = BytesIO()

    x = np.linspace(0, 2*np.pi, 101)
    y = np.sin(x)

    plt.plot(x, y)
    plt.grid()
    plt.xlabel('Angle [rad]')
    plt.ylabel('Amplitude')
    plt.xlim(x[0], x[-1])
    plt.savefig(img, format='png', transparent=True, pad_inches=0)
    plt.close()

    img.seek(0)
    img = base64.b64encode(img.getvalue()).decode()

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, figure=img)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Could not update that task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
