Football Data API

A Python-based API for football data that serves team and match information, and allows you to add new match data. This API provides endpoints for retrieving team information and match results, as well as adding new match results.

Structure

football_api
- backend
    - app.py        # API logic and endpoints
    - teams.csv     # CSV containing team information
    - matches.csv   # CSV containing match information
- frontend
    - index.html    # Frontend interface to display data and interact with the API

How to Use

Run the Backend:
  - Navigate to the backend directory and run the Flask application:
    python3 app.py
The API will be available at http://localhost:5000.

Access the Frontend:
  - Open the frontend/index.html file in a web browser to view and interact with the API.
