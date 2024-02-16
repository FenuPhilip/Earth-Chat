from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  # Change this to a secure secret key
socketio = SocketIO(app)

messages = []

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', messages=messages, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    messages.append({'username': username, 'message': message})
    emit('update_chat', {'messages': messages}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
