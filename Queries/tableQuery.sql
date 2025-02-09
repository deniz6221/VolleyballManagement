DROP DATABASE IF EXISTS VolleyballDatabase;
CREATE DATABASE VolleyballDatabase;
USE VolleyballDatabase;

CREATE TABLE Person(
    username varchar(512) PRIMARY KEY,
    password varchar(512),
    personType int
);

CREATE TABLE DatabaseManager(
    username varchar(512) PRIMARY KEY,
    password varchar(512),
    FOREIGN KEY (username) REFERENCES Person(username)
);

CREATE TABLE Player(
    username varchar(512) PRIMARY KEY,
    name varchar(512),
    surname varchar(512),
    password varchar(512),
    date_of_birth varchar(512),
    weight int,
    height int,
    FOREIGN KEY (username) REFERENCES Person(username)
);

CREATE TABLE Coach(
    username varchar(512) PRIMARY KEY,
    name varchar(512),
    surname varchar(512),
    password varchar(512),
    nationality varchar(512) NOT NULL,
    FOREIGN KEY (username) REFERENCES Person(username)
);

CREATE TABLE Jury(
    username varchar(512) PRIMARY KEY,
    name varchar(512),
    surname varchar(512),
    password varchar(512),
    nationality varchar(512) NOT NULL,
    FOREIGN KEY (username) REFERENCES Person(username)
);

CREATE TABLE Positions(
    position_id int PRIMARY KEY,
    position_name varchar(512)
);
CREATE TABLE Channel(
    channel_ID int PRIMARY KEY,
    channel_name varchar(512)
);


CREATE TABLE Team(
    team_id int PRIMARY KEY,
    team_name varchar(512),
    coach_username varchar(512) NOT NULL,
    contract_start varchar(512),
    contract_finish varchar(512),
    channel_ID int NOT NULL,
    FOREIGN KEY (channel_ID) REFERENCES Channel(channel_ID),
    FOREIGN KEY (coach_username) REFERENCES Coach(username)
);
CREATE TABLE Stadium(
    stadium_ID int PRIMARY KEY,
    stadium_name varchar(512) NOT NULL,
    stadium_country varchar(512) NOT NULL
);

CREATE TABLE MatchSession(
    session_ID int PRIMARY KEY,
    team_id int NOT NULL,
    time_slot int NOT NULL,
    match_date varchar(512) NOT NULL,
    assigned_jury_username varchar(512) NOT NULL,
    stadium_ID int NOT NULL,
    rating float,
    FOREIGN KEY (assigned_jury_username) REFERENCES Jury(username),
    FOREIGN KEY (stadium_ID) REFERENCES Stadium(stadium_ID)
);


CREATE TABLE PlayerPositions(
    player_positions_ID int AUTO_INCREMENT PRIMARY KEY,
    username varchar(512),
    position int,
    FOREIGN KEY (username) REFERENCES Player(username),
    FOREIGN KEY (position) REFERENCES Positions(position_id)
);

CREATE TABLE PlayerTeams(
    player_teams_id int AUTO_INCREMENT PRIMARY KEY,
    username varchar(512) NOT NULL,
    team int NOT NULL,
    FOREIGN KEY (username) REFERENCES Player(username),
    FOREIGN KEY (team) REFERENCES Team(team_id)

);

CREATE TABLE SessionSquads(
    squad_ID int AUTO_INCREMENT PRIMARY KEY,
    played_player_username varchar(512),
    session_ID int,
    position_ID int,
    FOREIGN KEY (played_player_username) REFERENCES Player(username),
    FOREIGN KEY (session_ID) REFERENCES MatchSession(session_ID)
    
);