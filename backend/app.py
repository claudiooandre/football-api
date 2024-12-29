import csv
from flask import Flask, jsonify, request

app = Flask(__name__)

# Function to load data from CSV
def load_csv(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# Load initial data from CSVs
teams = load_csv('./backend/teams.csv')
matches = load_csv('./backend/matches.csv')

# API Endpoints
@app.route('/teams', methods=['GET'])
def get_teams():
    return jsonify(teams)

@app.route('/matches', methods=['GET'])
def get_matches():
    return jsonify(matches)

@app.route('/set_match', methods=['POST'])
def add_match():
    # Data sent by the client
    new_match = request.json
    
    if not new_match:  # Check if JSON was sent
        return jsonify({"error": "No JSON sent or invalid JSON"}), 400

    # Check if all fields are present
    expected_fields = ["id", "team1", "team2", "score"]
    for field in expected_fields:
        if field not in new_match:
            return jsonify({"error": f"Field '{field}' is missing"}), 400

    # Add new match to the in-memory list
    matches.append(new_match)
    
    # Save to CSV file
    with open('./backend/matches.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=expected_fields)
        if f.tell() == 0:  # Add header if the file is empty
            writer.writeheader()
        writer.writerow(new_match)

    return jsonify({"message": "Match successfully added!"}), 201


if __name__ == '__main__':
    app.run(debug=True)
