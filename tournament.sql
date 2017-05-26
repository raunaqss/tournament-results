-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  name text,
  id serial primary key
);

CREATE TABLE matches (
  winner serial references players,
  loser serial references players,
  id serial primary key
);

CREATE VIEW score_board AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY wins DESC) AS rank
  FROM (SELECT p.id AS id,
               p.name AS name,
               count(m.id) AS wins
          FROM players AS p
               LEFT JOIN matches AS m
               ON p.id = m.winner
         GROUP BY p.id
         ORDER BY wins DESC) AS scores_without_ranks
);