import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import { useParams } from "react-router-dom";

const App = () => {
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState("");
  const [newSeason, setNewSeason] = useState("");
  const [teams, setTeams] = useState([]);
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [score, setScore] = useState("");
  const [league, setLeague] = useState("");
  const [season, setSeason] = useState("");

  // Carregar temporadas ao iniciar
  useEffect(() => {
    fetch("/seasons")
      .then((response) => response.json())
      .then((data) => {
        // Ordenar as épocas alfabeticamente antes de definir no estado
        const sortedSeasons = data.sort((a, b) => a.name.localeCompare(b.name));
        setSeasons(sortedSeasons);
      })
      .catch((error) => console.error("Erro ao carregar temporadas:", error));
  }, []);

  // Carregar equipes ao iniciar
  useEffect(() => {
    fetch("/teams")
      .then((response) => response.json())
      .then((data) => setTeams(data))
      .catch((error) => console.error("Erro ao carregar equipes:", error));
  }, []);

  // Adicionar nova temporada
  const handleAddSeason = () => {
    if (!newSeason) return alert("Digite um nome para a nova temporada!");

    fetch("/seasons", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ season: newSeason }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao adicionar temporada");
        }
        return response.json();
      })
      .then((data) => {
        alert(data.message);
        setSeasons([...seasons, { id: seasons.length + 1, name: newSeason }]);
        setNewSeason("");
      })
      .catch((error) => console.error(error));
  };

  // Adicionar nova partida
  const handleAddMatch = () => {
    if (!team1 || !team2 || !score || !season || !league) {
      return alert("Preencha todos os campos para adicionar um novo jogo!");
    }

    fetch("/matches", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ team1, team2, score, season, league }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao adicionar partida");
        }
        return response.json();
      })
      .then((data) => {
        alert(data.message);
        setTeam1("");
        setTeam2("");
        setScore("");
        setSeason("");
        setLeague("");
      })
      .catch((error) => console.error(error));
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Página principal */}
          <Route
            path="/"
            element={
              <>
                <h1>Football Data API</h1>

                <div className="add-season">
                  <h2>Add New Season</h2>
                  <input
                    type="text"
                    placeholder="Nova Temporada (e.g., 2025/2026)"
                    value={newSeason}
                    onChange={(e) => setNewSeason(e.target.value)}
                  />
                  <button onClick={handleAddSeason}>Add Season</button>
                </div>

                <div className="add-match">
                  <h2>Add New Match</h2>
                  <select value={team1} onChange={(e) => setTeam1(e.target.value)}>
                    <option value="">Select Team 1</option>
                    {teams.map((team) => (
                      <option key={team.id} value={team.id}>
                        {team.team}
                      </option>
                    ))}
                  </select>
                  <select value={team2} onChange={(e) => setTeam2(e.target.value)}>
                    <option value="">Select Team 2</option>
                    {teams.map((team) => (
                      <option key={team.id} value={team.id}>
                        {team.team}
                      </option>
                    ))}
                  </select>
                  <input
                    type="text"
                    placeholder="Score"
                    value={score}
                    onChange={(e) => setScore(e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="League"
                    value={league}
                    onChange={(e) => setLeague(e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="Season"
                    value={season}
                    onChange={(e) => setSeason(e.target.value)}
                  />
                  <button onClick={handleAddMatch}>Add Match</button>
                </div>

                <div className="seasons">
                  <h2>Seasons</h2>
                  <select
                    onChange={(e) => setSelectedSeason(e.target.value)}
                    value={selectedSeason}
                  >
                    <option value="">Select Season</option>
                    {seasons.map((season) => (
                      <option key={season.id} value={season.name}>
                        {season.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Links para páginas de Equipas e Matches */}
                <div className="links">
                  <Link to={`/teams?season=${selectedSeason}`}>
                    View Teams
                  </Link>
                  <br />
                  <Link to={`/matches?season=${selectedSeason}`}>
                    View Matches
                  </Link>
                </div>
              </>
            }
          />

          {/* Página de Equipas */}
          <Route path="/teams" element={<Teams />} />

          {/* Página de Matches */}
          <Route path="/matches" element={<Matches />} />

          {/* Página de detalhes do time */}
          <Route path="/teams/:id" element={<TeamDetails />} />

          {/* Página de detalhes da partida */}
          <Route path="/matches/:id" element={<MatchDetails />} />
        </Routes>
      </div>
    </Router>
  );
};

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const params = new URLSearchParams(window.location.search);
  const season = params.get("season");

  useEffect(() => {
    fetch(`/teams?season=${season}`)
      .then((response) => response.json())
      .then((data) => setTeams(data))
      .catch((error) => console.error("Erro ao carregar equipes:", error));
  }, [season]);

  if (!season) {
    return <div>Please select a season on the main page.</div>;
  }

  return (
    <div>
      <h2>Teams in {season}</h2>
      <table>
        <thead>
          <tr>
            <th>Team</th>
            <th>Country</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((team) => (
            <tr key={team.id}>
              <td>
                <Link to={`/teams/${team.id}`}>{team.team}</Link>
              </td>
              <td>{team.country}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const Matches = () => {
  const [matches, setMatches] = useState([]);
  const [teams, setTeams] = useState([]);
  const params = new URLSearchParams(window.location.search);
  const selectedSeason = params.get("season");

  useEffect(() => {
    fetch(`/matches?season=${selectedSeason}`)
      .then((response) => response.json())
      .then((data) => setMatches(data))
      .catch((error) => console.error("Erro ao carregar partidas:", error));
  }, [selectedSeason]);

  useEffect(() => {
    fetch(`/teams`)
      .then((response) => response.json())
      .then((data) => setTeams(data))
      .catch((error) => console.error("Erro ao carregar equipes:", error));
  }, []);

  const getTeamName = (teamId) => {
    const team = teams.find((team) => team.id === teamId);
    return team ? team.team : "Unknown";
  };

  if (!selectedSeason) {
    return <div>Please select a season on the main page.</div>;
  }

  return (
    <div>
      <h2>Matches in {selectedSeason}</h2>
      <table>
        <thead>
          <tr>
            <th>Team 1</th>
            <th>Team 2</th>
            <th>Score</th>
            <th>League</th>
          </tr>
        </thead>
        <tbody>
          {matches.map((match) => (
            <tr key={match.id}>
              <td>
                <Link to={`/teams/${match.team1}`}>{getTeamName(match.team1)}</Link>
              </td>
              <td>
                <Link to={`/teams/${match.team2}`}>{getTeamName(match.team2)}</Link>
              </td>
              <td>{match.score}</td>
              <td>{match.league}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const TeamDetails = () => {
  const { id } = useParams();
  const [team, setTeam] = useState(null);

  useEffect(() => {
    fetch(`/teams/${id}`)
      .then((response) => response.json())
      .then((data) => setTeam(data))
      .catch((error) => console.error("Erro ao carregar detalhes do time:", error));
  }, [id]);

  if (!team) return <div>Loading...</div>;

  return (
    <div>
      <h2>Detalhes do Time</h2>
      <p>Nome: {team.team}</p>
      <p>País: {team.country}</p>
    </div>
  );
};

const MatchDetails = () => {
  const { id } = useParams();
  const [match, setMatch] = useState(null);
  const [team1Name, setTeam1Name] = useState("");
  const [team2Name, setTeam2Name] = useState("");

  useEffect(() => {
    fetch(`/matches/${id}`)
      .then((response) => response.json())
      .then((data) => {
        setMatch(data);
        fetch(`/teams/${data.team1}`)
          .then((response) => response.json())
          .then((team1Data) => setTeam1Name(team1Data.team));
        fetch(`/teams/${data.team2}`)
          .then((response) => response.json())
          .then((team2Data) => setTeam2Name(team2Data.team));
      })
      .catch((error) => console.error("Erro ao carregar detalhes da partida:", error));
  }, [id]);

  if (!match) return <div>Loading...</div>;

  return (
    <div>
      <h2>Detalhes da Partida</h2>
      <p>ID: {match.id}</p>
      <p>Time 1: {team1Name}</p>
      <p>Time 2: {team2Name}</p>
      <p>Placar: {match.score}</p>
      <p>Liga: {match.league}</p>
      <p>Temporada: {match.season}</p>
    </div>
  );
};

export default App;