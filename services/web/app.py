from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

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

@app.route('/api/news')
def get_news():
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
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Mock login logic
    if username == 'user' and password == 'pass':
        return jsonify({'success': True, 'message': 'Login successful.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

@app.route('/icon.png')
def favicon():
    return send_from_directory('.', 'icon.png')

@app.route('/icon.ico')
def favicon_ico():
    return redirect(url_for('static', filename='icon.ico'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
