from flask import Flask, request, jsonify
from db import db, init_db, Story, User, Session
from secrets import token_urlsafe
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thewire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

@app.route('/api/stories', methods=['POST'])
def add_stories():
    data = request.get_json()
    # Expecting a JSON object with broadcast_metadata and stories
    meta = data.get('broadcast_metadata', {})
    stories = data.get('stories', [])
    inserted = []
    for s in stories:
        story = Story(
            broadcast_date=meta.get('date'),
            broadcast_time=meta.get('time'),
            precedence=meta.get('precedence'),
            information_cutoff=meta.get('information_cutoff'),
            topic=s['metadata'].get('topic'),
            title=s['metadata'].get('title'),
            tldr=s['metadata'].get('tldr'),
            story_date=s['metadata'].get('date'),
            story_time=s['metadata'].get('time'),
            text=s.get('text')
        )
        db.session.add(story)
        inserted.append(story)
    db.session.commit()
    return jsonify({'inserted': [s.id for s in inserted]}), 201

@app.route('/api/stories', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify([
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
        } for s in stories
    ])

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], email=data.get('email'))
    user.set_password(data['password'])
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400
    return jsonify({'id': user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        # Generate a secure session token
        session_token = token_urlsafe(32)
        session = Session(user_id=user.id, ip_address=request.remote_addr, token=session_token)
        db.session.add(session)
        db.session.commit()
        return jsonify({'message': 'Login successful', 'user_id': user.id, 'token': session_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    token = data.get('token')
    session = Session.query.filter_by(token=token).first()
    if session:
        user = User.query.get(session.user_id)
        return jsonify({'valid': True, 'user_id': user.id, 'username': user.username, 'login_time': session.login_time.isoformat()}), 200
    return jsonify({'valid': False}), 401

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    sessions = Session.query.all()
    return jsonify([
        {
            'id': s.id,
            'user_id': s.user_id,
            'login_time': s.login_time.isoformat(),
            'ip_address': s.ip_address
        } for s in sessions
    ])

@app.route('/api/dump_stories', methods=['GET'])
def dump_stories():
    """Dump all stories in the database for debugging purposes."""
    stories = Story.query.all()
    return jsonify([
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
        } for s in stories
    ])

@app.route('/api/clear_db', methods=['POST'])
def clear_db():
    """Delete all stories, users, and sessions from the database. For development/debug only!"""
    Story.query.delete()
    Session.query.delete()
    User.query.delete()
    db.session.commit()
    return jsonify({'status': 'Database cleared!'}), 200

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    app.run(debug=True, host='0.0.0.0', port=5000)
