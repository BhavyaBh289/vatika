from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    users = get_users()
    return render_template('index.html', users=users)

@app.route('/give_points', methods=['POST'])
def give_points():
    username = request.form.get('username')
    points_attendence = int(request.form.get('points_attendence'))
    points_gatha = int(request.form.get('points_gatha'))

    give_user_points(username, points_attendence, points_gatha)
    return redirect(url_for('index'))

def get_users():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)

    with open('users.json', 'r') as f:
        return json.load(f)

def give_user_points(username, points_attendence, points_gatha):
    users = get_users()
    if username in users:
        users[username]['points_attendence'] += points_attendence
        users[username]['points_gatha'] += points_gatha
        users[username]['cumulative_points'] = users[username]['points_attendence'] + users[username]['points_gatha']
    else:
        users[username] = {
            'points_attendence': points_attendence,
            'points_gatha': points_gatha,
            'cumulative_points': points_attendence + points_gatha
        }

    with open('users.json', 'w') as f:
        json.dump(users, f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
