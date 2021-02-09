from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os, functions
app = Flask(__name__)

db_uri = os.environ.get('DATABASE_URL') or "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    header = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)
    count = db.Column(db.Integer)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts, today=date.today())
    else:
        title = request.form.get('title')
        header = functions.shrinktitle(title)
        detail = request.form.get('detail')
        due = date.today()
        count = 0

        new_post = Post(title=title, header=header, detail=detail, due=due, count=count)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)


@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')

        db.session.commit()
        return redirect('/')


@app.route('/count_plus/<int:id>')
def count_plus(id):
    post = Post.query.get(id)
    if post.count >= 3:
        db.session.delete(post)
    else:
        post.count = post.count + 1
        post.due = date.today()
    db.session.commit()
    return redirect('/')


@app.route('/count_minus/<int:id>')
def count_minus(id):
    post = Post.query.get(id)
    if post.count > 0:
        post.count = post.count - 1
    post.due = date.today()
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
