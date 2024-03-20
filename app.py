from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_username():
    if request.method == 'POST':
        username = request.form.get('username')
        users = get_users()
        if username in users:
            return redirect(url_for('view_points', username=username))
        else:
            return "User not found"
    else:
        return render_template('get_username.html')

@app.route('/admin')
def admin_index():
    users = get_users()
    return render_template('admin_index.html', users=users)

@app.route('/admin/give_points', methods=['POST'])
def give_points():
    username = request.form.get('username')
    points_attendance = int(request.form.get('points_attendance'))
    points_gatha = int(request.form.get('points_gatha'))

    give_user_points(username, points_attendance, points_gatha)
    return redirect(url_for('admin_index'))

@app.route('/view_points/<username>')
def view_points(username):
    users = get_users()
    if username in users:
        user = users[username]
        return render_template('view_points.html', username=username, user=user)
    else:
        return "User not found"

def get_users():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)

    with open('users.json', 'r') as f:
        return json.load(f)

def give_user_points(username, points_attendance, points_gatha):
    users = get_users()
    if username in users:
        users[username]['points_attendance'] += points_attendance
        users[username]['points_gatha'] += points_gatha
        users[username]['cumulative_points'] = users[username]['points_attendance'] + users[username]['points_gatha']
    else:
        users[username] = {
            'points_attendance': points_attendance,
            'points_gatha': points_gatha,
            'cumulative_points': points_attendance + points_gatha
        }

    with open('users.json', 'w') as f:
        json.dump(users, f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
