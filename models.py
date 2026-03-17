from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    status = db.Column(db.String(20), default='inactive')
    posts = db.relationship('Post', backref='author', lazy=True)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('posts', lazy=True))