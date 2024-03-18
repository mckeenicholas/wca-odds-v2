SET SEARCH_PATH to wca_results

\copy Competitions (id, year, month, day) FROM 'results_dump/Competitions.csv' DELIMITER ',' CSV HEADER; 

\copy Results (competitionId, eventId, roundTypeId, personName, personId, formatId, value1, value2, value3, value4, value5) FROM 'results_dump/Results.csv' DELIMITER ',' CSV HEADER; 
