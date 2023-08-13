import csv
import os
import random
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import threading

app = Flask(__name__)
socketio = SocketIO(app)

current_process = None


@app.route('/')
def display_data():
    """Display data from CSV with optional search query."""
    data = read_csv()
    search_query = request.args.get('search', '').lower()
    data = [row for row in data if search_query in row.get('human_name', '').lower()]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data=data)
    else:
        return render_template('index.html', data=data)


@app.route('/random')
def random_key():
    """Get a random key."""
    data = read_csv()
    return render_template('index.html', data=[random.choice(data)]) if data else redirect(url_for('display_data'))


def get_latest_csv():
    """Retrieve the latest CSV filename based on naming pattern."""
    files = [f for f in os.listdir('.') if f.startswith('humble_export_') and f.endswith('.csv')]
    return max(files, default=None)


def read_csv():
    """Read content from the latest CSV."""
    filename = get_latest_csv()
    if not filename:
        return []

    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return [{key.strip(): value.strip() for key, value in row.items()} for row in reader if row.get('redeemed_key_val') != "Redeemed to MoyJak"]


def run_script():
    print("Starting script2")
    global current_process
    current_process = subprocess.Popen(['cmd.exe', '/c', 'run_redeemer.bat'],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True)

    while True:
        output = current_process.stdout.readline().strip()
        error_output = current_process.stderr.readline().strip()
        if error_output:
            socketio.emit('script_error_output', {'data': error_output})
        if output == '' and current_process.poll() is not None:
            break
        if output:
            socketio.emit('script_output', {'data': output})


@socketio.on('send_input')
def handle_input(message):
    global current_process
    current_process.stdin.write(message['data'] + "\n")
    current_process.stdin.flush()


@socketio.on('start_script')
def handle_start():
    print("Starting script")
    thread = threading.Thread(target=run_script)
    thread.start()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)

