import csv
import os
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)


@app.route('/')
def display_data():
    data = read_csv()
    platform = request.args.get('platform', '')
    search_query = request.args.get('search', '').lower()

    if platform:
        data = [row for row in data if row.get('key_type_human_name', '').strip() == platform]
    if search_query:
        data = [row for row in data if search_query in row.get('human_name', '').lower()]

    platforms = set(row.get('key_type_human_name', '') for row in data)

    # Check if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data=data)

    return render_template('index.html', data=data, platforms=platforms)


@app.route('/random')
def random_key():
    data = read_csv()
    if not data:
        return redirect(url_for('display_data'))
    random_choice = random.choice(data)
    return render_template('index.html', data=[random_choice], platforms=set())


def get_latest_csv():
    files = [f for f in os.listdir('.') if f.startswith('humble_export_') and f.endswith('.csv')]
    files.sort(reverse=True)
    return files[0] if files else None


def read_csv():
    filename = get_latest_csv()
    if filename is None:
        return []

    data = []
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
            if cleaned_row.get('redeemed_key_val') != "Redeemed to MoyJak":
                data.append(cleaned_row)

    return data


if __name__ == '__main__':
    app.run(debug=True)
