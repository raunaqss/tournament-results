#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    query = 'DELETE FROM matches;'
    c.execute(query)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    query = 'DELETE FROM players;'
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    query = 'SELECT count(id) FROM players;'
    c.execute(query)
    response = c.fetchone()
    conn.close()
    return response[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    query = 'INSERT INTO players VALUES (%s)'
    data = (name, )
    c.execute(query, data)
    conn.commit()
    conn.close()
    

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = '''
    SELECT p.id, p.name, count(m1.id) AS wins, count(m2.id) AS total
      FROM players AS p
           LEFT JOIN matches AS m1
                  ON p.id = m1.winner
           LEFT JOIN matches AS m2
                  ON p.id = m2.winner
                  OR p.id = m2.loser
     GROUP BY p.id
     ORDER BY wins DESC;
    '''
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    query = '''
    INSERT INTO matches VALUES (%s, %s);
    '''
    data = (winner, loser, )
    c.execute(query, data)
    conn.commit()
    conn.close() 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    query = '''
    SELECT p1.id, p1.name, p2.id, p2.name
      FROM score_board AS p1,
           score_board AS p2
     WHERE p2.rank - p1.rank = 1
       AND p2.rank % 2 = 0;
    '''
    c.execute(query);
    result = c.fetchall()
    conn.close()
    return result


