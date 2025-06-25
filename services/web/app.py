from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session, make_response
from datetime import datetime, timedelta
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session cookies (change in production)

# Mock database (replace with real DB calls)
mock_articles = [
    {
        "id": i,
        "title": f"News Article {i}",
        "content": f"This is the summary of news article {i}.",
        "published_at": (datetime.now() - timedelta(minutes=i)).isoformat()
    }
    for i in range(1, 101)
]

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    resp = requests.post('http://localhost:5000/api/register', json=data)
    if resp.status_code == 201:
        return jsonify({'success': True, 'message': 'Account created! You can now log in.'}), 201
    else:
        try:
            return jsonify(resp.json()), resp.status_code
        except Exception:
            return jsonify({'success': False, 'message': 'Registration failed.'}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    resp = requests.post('http://localhost:5000/api/login', json=data)
    if resp.status_code == 200:
        token = resp.json().get('token')
        response = jsonify({'success': True, 'token': token, 'message': 'Login successful.'})
        response.set_cookie('session_token', token, httponly=True)
        return response
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

def get_token():
    token = request.cookies.get('session_token')
    if not token:
        token = request.headers.get('Authorization')
    return token

@app.route('/api/news')
def get_news():
    token = get_token()
    if not token:
        return jsonify({'error': 'Not authenticated'}), 401
    # Validate token with API
    valid = requests.post('http://localhost:5000/api/validate', json={'token': token})
    if valid.status_code != 200 or not valid.json().get('valid'):
        return jsonify({'error': 'Invalid session'}), 401
    limit = int(request.args.get('limit', 10))
    before = request.args.get('before')
    # Fetch stories from the real API/database service
    try:
        api_url = 'http://localhost:5000/api/stories'
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return jsonify({'error': 'Failed to fetch news from database.'}), 500
        stories = resp.json()
        # Just use the date and time as strings from the database
        for s in stories:
            s['published_at'] = f"{s.get('broadcast_date','')} {s.get('broadcast_time','')}".strip()
            s['content'] = s.get('tldr') or (s.get('text','')[:200])
            s['full_story'] = s.get('text','')
        # Filter by 'before' timestamp if provided
        if before:
            stories = [a for a in stories if a['published_at'] < before]
        sorted_articles = sorted(stories, key=lambda x: x['published_at'], reverse=True)
        return jsonify(sorted_articles[:limit])
    except Exception as e:
        return jsonify({'error': f'Exception fetching news: {e}'}), 500

@app.route('/')
def root_redirect():
    return redirect(url_for('serve_login'))

@app.route('/login')
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route('/news')
def serve_news():
    token = get_token()
    if not token:
        return redirect(url_for('serve_login'))
    valid = requests.post('http://localhost:5000/api/validate', json={'token': token})
    if valid.status_code != 200 or not valid.json().get('valid'):
        return redirect(url_for('serve_login'))
    return send_from_directory('.', 'index.html')

@app.route('/icon.png')
def favicon():
    return send_from_directory('.', 'icon.png')


if __name__ == '__main__':
    app.run(debug=False, port=8000, host='0.0.0.0')
