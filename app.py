from flask import Flask, render_template, url_for
from database import db
from models import User, Post, Comment
from forms import SignUpForm
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


@app.route('/signup', methods=['post', 'get'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        u = User()
        u.username = form.username.data
        u.password = form.password.data
        u.email = form.email.data

        db.session.add(u)
        db.session.commit()
        return "success"

    print("Current Errors:")
    print(form.errors)

    return render_template('signup.html', form=form)


@app.route('/')
def home():
    p = Post.query.order_by(Post.dttm.desc()).all()
    return render_template('home.html', posts=p)


@app.route('/post/<int:id>')
def post(id):
    p = Post.query.filter_by(id=id).first_or_404()
    return render_template('post.html', post=p)


@app.route('/user/<string:username>')
def user(username):

    print(username)
    # u = User.query.filter(User.username == username).first()
    # u = User.query.filter_by(username=username).first()

    p = Post.query.join(User).filter(User.username == username).all()

    # SELECT * FROM POSTS
    # WHERE POSTS.user_id = USER.id
    # AND USER.username = 'anthony'

    return render_template('user.html', posts=p, username=username)


if __name__ == '__main__':
    app.run()
