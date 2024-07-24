import pandas as pd 
import os
import berserk 
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta 

# load the token
lichess_token = os.getenv("LICHESS_TOKEN")

# initalize the session and client
session = berserk.TokenSession(lichess_token)
client = berserk.Client(session=session)

def gettop10players(chess_category) -> pd.DataFrame:
    """
    
        Function to get top 10 players in chess category on lichess based on lichess rating. 
    
    """
   
    # get top 10 players from all categories
    top10_players = client.users.get_all_top_10() 
    
    # select the top 10 of one category 
    top10_category = pd.json_normalize(top10_players, record_path=chess_category).rename(
                      columns={f"perfs.{chess_category}.rating" : f"{chess_category}_rating", f"perfs.{chess_category}.progress" : f"{chess_category}_progress"}) 
    
    # return 
    return top10_category

def getrecord_top10(chess_category) -> pd.DataFrame:
    """
    
        Function to get record of top 10 classic players in last 12 months
    
    """  
    
    # take the id
    players_id = gettop10players(chess_category)["id"]
    
    # last day of last month as last date 
    last_date = datetime.today().replace(day=1) - timedelta(days=1) 

    # date 12 months before
    date_11_months_before = last_date - relativedelta(months=11)

    # first day of the last 11 months as first date
    first_date = date_11_months_before.replace(day=1)
    
    start = berserk.utils.to_millis(first_date)
    end = berserk.utils.to_millis(last_date)

    # using polar for speed
    topplayers_games = pd.json_normalize(client.games.export_by_player(players_id[0], since=start, until=end))
    
    for i in range(1, 10) :
        # list of game
        games_df = pd.json_normalize(client.games.export_by_player(players_id[i], since=start, until=end))
        topplayers_games = pd.concat([topplayers_games, games_df])

    # only choose useful index
    cols_selection = list(range(1,4)) + list(range(7,8)) + list(range(9,11)) + list(range(12,13)) + list(range(14,16)) + list(range(19,21))
    return topplayers_games.iloc[:, cols_selection]

def save_record(dataframe, filename):
    """
    Function to save a dataframe to a CSV file in the 'lichess-record-data' directory.
    """
    directory = 'lichess-record-data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    dataframe.to_csv(file_path, index=False)
    print(f"Data written to {file_path}")

def getrecord_classical():
    """
    Function to get records of top 10 players in classic chess.
    """
    classical_record = getrecord_top10("classical")
    save_record(classical_record, "top10-classical-record.csv")

def getrecord_rapid():
    """
    Function to get records of top 10 players in rapid chess.
    """
    rapid_record = getrecord_top10("rapid")
    save_record(rapid_record, "top10-rapid-record.csv")

def getrecord_blitz():
    """
    Function to get records of top 10 players in blitz chess.
    """
    blitz_record = getrecord_top10("blitz")
    save_record(blitz_record, "top10-blitz-record.csv")

def getrecord_bullet():
    """
    Function to get records of top 10 players in bullet chess.
    """
    bullet_record = getrecord_top10("bullet")
    save_record(bullet_record, "top10-bullet-record.csv")

def getrecord_ultrabullet():
    """
    Function to get records of top 10 players in ultra bullet chess.
    """
    ultrabullet_record = getrecord_top10("ultraBullet")
    save_record(ultrabullet_record, "top10-ultrabullet-record.csv")