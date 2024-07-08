import pandas as pd 
import polars as pl
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

def getrecord_top10(chess_category) -> pl.DataFrame:
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
    games_list_df = pd.json_normalize(client.games.export_by_player(players_id[0], since=start, until=end))
    topplayers_games = pl.DataFrame(games_list_df)
    
    for i in range(1, 10) :
        # list of game
        games_list2 = client.games.export_by_player(players_id[i], since=start, until=end)
        games_list_df2 = pd.json_normalize(games_list_df)
        topplayers_games = topplayers_games.vstack(games_list_df2)

    return topplayers_games
    
def getrecord_classical(): 
    """
    
        Function to get records of top 10 players in classic chess
    
    """
    
    classical_record_df = getrecord_top10("classical")
    classical_record_df.write_parquet("data/top10-classical-record.parquet")

def getrecord_rapid(): 
    """
    
        Function to get records of top 10 players in rapid chess
    
    """
    
    rapid_record_df = getrecord_top10("rapid")
    rapid_record_df.write_parquet("data/top10-rapid-record.parquet")
    
def getrecord_blitz(): 
    """
    
        Function to get records of top 10 players in blitz chess
    
    """
    
    blitz_record_df = getrecord_top10("blitz")
    blitz_record_df.write_parquet("data/top10-blitz-record.parquet")
    
def getrecord_bullet(): 
    """
    
        Function to get records of top 10 players in bullet chess
    
    """
    
    bullet_record_df = getrecord_top10("bullet")
    bullet_record_df.write_parquet("data/top10-bullet-record.parquet")
    
def getrecord_ultrabullet(): 
    """
    
        Function to get records of top 10 players in ultra bullet chess
    
    """
    
    ultrabullet_record_df = getrecord_top10("ultraBullet")
    ultrabullet_record_df.write_parquet("data/top10-ultrabullet-record.parquet")