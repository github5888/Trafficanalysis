
from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vehicle_data')
def vehicle_data():
    data = []
    with open('traffic_pattern_final.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({'frame': int(row['Frame']), 'count': int(row['Vehicle Count'])})
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)