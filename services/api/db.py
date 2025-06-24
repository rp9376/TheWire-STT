from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from passlib.hash import bcrypt
from datetime import datetime
from secrets import token_urlsafe

db = SQLAlchemy()

def init_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broadcast_date = db.Column(db.String(20))
    broadcast_time = db.Column(db.String(20))
    precedence = db.Column(db.String(20))
    information_cutoff = db.Column(db.String(20))
    topic = db.Column(db.String(100))
    title = db.Column(db.String(200))
    tldr = db.Column(db.String(500))
    story_date = db.Column(db.String(20))
    story_time = db.Column(db.String(20))
    text = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    token = db.Column(db.String(128), unique=True, nullable=False)

def dump_all_stories():
    """Return all stories as a list of dicts."""
    return [
        {
            'id': s.id,
            'broadcast_date': s.broadcast_date,
            'broadcast_time': s.broadcast_time,
            'precedence': s.precedence,
            'information_cutoff': s.information_cutoff,
            'topic': s.topic,
            'title': s.title,
            'tldr': s.tldr,
            'story_date': s.story_date,
            'story_time': s.story_time,
            'text': s.text
        } for s in Story.query.all()
    ]

def dump_all_users():
    """Return all users as a list of dicts (excluding password hashes)."""
    return [
        {
            'id': u.id,
            'username': u.username,
            'email': u.email
        } for u in User.query.all()
    ]

def dump_all_sessions():
    """Return all sessions as a list of dicts."""
    return [
        {
            'id': s.id,
            'user_id': s.user_id,
            'login_time': s.login_time.isoformat() if s.login_time else None,
            'ip_address': s.ip_address,
            'token': s.token
        } for s in Session.query.all()
    ]
