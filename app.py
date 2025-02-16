from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to the CSV files
TEAMS_CSV = os.path.join(BASE_DIR, "teams.csv")
MATCHES_CSV = os.path.join(BASE_DIR, "matches.csv")
SEASONS_CSV = os.path.join(BASE_DIR, "season.csv")
LEAGUES_CSV = os.path.join(BASE_DIR, "leagues.csv")  # New file for leagues

# Helper function to read CSV files
def read_csv(file_path):
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

# Helper function to write CSV files
def write_csv(file_path, fieldnames, data):
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Endpoint to get teams
@app.route("/teams", methods=["GET"])
def get_teams():
    season = request.args.get("season")
    teams = read_csv(TEAMS_CSV)

    if season:
        # Filter teams by season in the teams.csv file
        teams = [team for team in teams if team["season"] == season]

    return jsonify(teams)

# Endpoint to get matches
@app.route("/matches", methods=["GET"])
def get_matches():
    season = request.args.get("season")
    matches = read_csv(MATCHES_CSV)

    if season:
        # Filter matches by season
        matches = [match for match in matches if match["season"] == season]

    return jsonify(matches)

# Endpoint to add a new match
@app.route("/matches", methods=["POST"])
def add_match():
    data = request.get_json()
    team1 = data.get("team1")
    team2 = data.get("team2")
    score = data.get("score")
    season = data.get("season")
    league = data.get("league")

    if not all([team1, team2, score, season, league]):
        return jsonify({"error": "All fields are required"}), 400

    teams = read_csv(TEAMS_CSV)
    if not any(team["id"] == team1 for team in teams) or not any(team["id"] == team2 for team in teams):
        return jsonify({"error": "One or both teams not found"}), 400

    matches = read_csv(MATCHES_CSV)
    new_match = {
        "id": str(len(matches) + 1),
        "team1": team1,
        "team2": team2,
        "score": score,
        "season": season,
        "league": league
    }
    matches.append(new_match)
    write_csv(MATCHES_CSV, fieldnames=["id", "team1", "team2", "score", "season", "league"], data=matches)
    return jsonify({"message": "Match added successfully!"}), 201

# Endpoint to list seasons
@app.route("/seasons", methods=["GET"])
def get_seasons():
    seasons = read_csv(SEASONS_CSV)
    return jsonify(seasons)

# Endpoint to add a new season
@app.route("/seasons", methods=["POST"])
def add_season():
    data = request.get_json()
    new_season = data.get("season")
    if new_season:
        seasons = read_csv(SEASONS_CSV)
        # Check if the season already exists
        if any(season.get("name") == new_season for season in seasons):
            return jsonify({"error": "Season already exists"}), 400

        # Add new season
        seasons.append({"id": str(len(seasons) + 1), "name": new_season})
        write_csv(SEASONS_CSV, fieldnames=["id", "name"], data=seasons)
        return jsonify({"message": f"Season '{new_season}' added successfully!"}), 201

    return jsonify({"error": "Season name is required"}), 400

# Endpoint to list leagues
@app.route("/leagues", methods=["GET"])
def get_leagues():
    leagues = read_csv(LEAGUES_CSV)
    return jsonify(leagues)

# Endpoint to add a new league
@app.route("/leagues", methods=["POST"])
def add_league():
    data = request.get_json()
    new_league = data.get("league")
    if new_league:
        leagues = read_csv(LEAGUES_CSV)
        # Check if the league already exists
        if any(league.get("name") == new_league for league in leagues):
            return jsonify({"error": "League already exists"}), 400

        # Add new league
        leagues.append({"id": str(len(leagues) + 1), "name": new_league})
        write_csv(LEAGUES_CSV, fieldnames=["id", "name"], data=leagues)
        return jsonify({"message": f"League '{new_league}' added successfully!"}), 201

    return jsonify({"error": "League name is required"}), 400

# Endpoint to get team details
@app.route("/teams/<id>", methods=["GET"])
def get_team_by_id(id):
    teams = read_csv(TEAMS_CSV)
    team = next((team for team in teams if team["id"] == id), None)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(team)

# Endpoint to get match details
@app.route("/matches/<id>", methods=["GET"])
def get_match_by_id(id):
    matches = read_csv(MATCHES_CSV)
    match = next((match for match in matches if match["id"] == id), None)
    if not match:
        return jsonify({"error": "Match not found"}), 404
    return jsonify(match)

if __name__ == "__main__":
    app.run(debug=True)