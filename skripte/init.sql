-- Erstellen der Tabelle 'players'
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    federation_code VARCHAR(5),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender INTEGER CHECK (gender IN (0, 1, 3)),
    plays_beach BOOLEAN,
    plays_volley BOOLEAN,
    team_name VARCHAR(100),
    no INTEGER UNIQUE
);

-- Erstellen der Tabelle 'beach_teams'
CREATE TABLE beach_teams (
    id SERIAL PRIMARY KEY,
    player1_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    player2_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    name VARCHAR(255),
    rank INTEGER,
    earned_points_team INTEGER,
    earnings_team INTEGER,
    no INTEGER UNIQUE,
    version INTEGER
);

-- Erstellen der Tabelle 'beach_rounds'
CREATE TABLE beach_rounds (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10),
    name VARCHAR(255),
    bracket VARCHAR(10),
    phase VARCHAR(10),
    start_date DATE,
    end_date DATE,
    number INTEGER UNIQUE,
    version INTEGER
);

-- Erstellen der Tabelle 'beach_matches'
CREATE TABLE beach_matches (
    id SERIAL PRIMARY KEY,
    no_in_tournament INTEGER,
    local_date DATE,
    local_time TIME,
    team_a_id INTEGER REFERENCES beach_teams(id) ON DELETE CASCADE,
    team_b_id INTEGER REFERENCES beach_teams(id) ON DELETE CASCADE,
    court VARCHAR(10),
    match_points_a INTEGER,
    match_points_b INTEGER,
    points_team_a_set1 INTEGER,
    points_team_b_set1 INTEGER,
    points_team_a_set2 INTEGER,
    points_team_b_set2 INTEGER,
    points_team_a_set3 INTEGER,
    points_team_b_set3 INTEGER,
    duration_set1 INTEGER,
    duration_set2 INTEGER,
    duration_set3 INTEGER,
    no_round_id INTEGER REFERENCES beach_rounds(id) ON DELETE CASCADE,
    no_tournament INTEGER,
    no_player_a1_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    no_player_a2_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    no_player_b1_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    no_player_b2_id INTEGER REFERENCES players(id) ON DELETE CASCADE
);
