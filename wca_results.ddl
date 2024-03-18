DROP SCHEMA IF EXISTS wca_results CASCADE;
CREATE SCHEMA wca_results;
SET search_path TO wca_results;

CREATE TYPE wca_results.event AS ENUM (
    '333', '222', '444', '555', '666', '777', '333oh', '333bf', '333fm', 'pyram', 'minx', 'skewb', 'sq1', 'clock', '333mbf', '444bf', '555bf', '333mbo', '333ft', 'magic', 'mmagic'
);

CREATE TABLE IF NOT EXISTS Competitions (
    id TEXT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Results (
    competitionId TEXT NOT NULL,
    eventId event NOT NULL,
    roundTypeId CHAR NOT NULL,
    personName TEXT NOT NULL,
    personId VARCHAR(10) NOT NULL,
    formatId CHAR NOT NULL,
    value1 INT,
    value2 INT,
    value3 INT,
    value4 INT,
    value5 INT,
    PRIMARY KEY(competitionId, eventId, roundTypeId, personId),
    FOREIGN KEY(competitionId) REFERENCES Competitions(id)
);
