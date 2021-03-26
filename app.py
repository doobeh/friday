from flask import Flask, render_template, url_for
from database import db
from models import User, Post, Comment
from faker import Faker
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///example.sqlite3'
app.config["SQLALCHEMY_ECHO"] = False
app.secret_key = 'SSHasdasd'
db.init_app(app)


@app.cli.command("start")
def start():
    fake = Faker()
    db.drop_all()
    db.create_all()

    # Users
    for _ in range(100):
        u = User()
        u.username = fake.unique.user_name()
        u.password = fake.password()
        u.email = fake.email()
        db.session.add(u)
    db.session.commit()

    # Posts
    all_users = User.query.all()
    for _ in range(1000):
        p = Post()
        p.user = random.choice(all_users)
        p.title = fake.sentence()
        p.content = fake.paragraph()
        db.session.add(p)
    db.session.commit()

    # Comments
    all_posts = Post.query.all()
    for _ in range(5000):
        c = Comment()
        c.content = fake.paragraph()
        c.user = random.choice(all_users)
        c.post = random.choice(all_posts)
        db.session.add(c)
    db.session.commit()


@app.errorhandler(404)
def error_page(id):
    return render_template('404.html'), 404


@app.route('/')
def home():
    p = Post.query.order_by(Post.dttm.desc()).all()
    return render_template('home.html', posts=p)


@app.route('/post/<int:id>')
def post(id):
    p = Post.query.filter_by(id=id).first_or_404()
    return render_template('post.html', post=p)





if __name__ == '__main__':
    app.run()
