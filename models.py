from database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return self.username


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='posts')
    title = db.Column(db.String)
    content = db.Column(db.String)
    dttm = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"{self.title} by {self.user.username}"


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='comments')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='comments')
    content = db.Column(db.String)
    dttm = db.Column(db.DateTime, default=datetime.now())

