SET SEARCH_PATH to wca_results

\copy Competitions (id, year, month, day) FROM 'Competitions.csv' DELIMITER ',' CSV HEADER; 

\copy Results (competitionId, eventId, roundTypeId, personName, personId, formatId, value1, value2, value3, value4, value5) FROM 'Results.csv' DELIMITER ',' CSV HEADER; 
