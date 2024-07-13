import pandas as pd
import os

# web crawling packages
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from lxml import html
import urllib.request
from html_table_parser.parser import HTMLTableParser
from pprint import pprint

## we can add in the selenium crawler if we want

## Opens a website and read its
# binary contents (HTTP Response Body)
def url_get_contents(url):

    # Opens a website and read its
    # binary contents (HTTP Response Body)

    #making request to the website
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)

    #reading contents of the website
    return f.read()

## parse stat tables
def game_stat_parser(url):
    
    try:
        # defining the html contents of a URL.
        xhtml = url_get_contents(url).decode('utf-8')

        # Defining the HTMLTableParser object
        p = HTMLTableParser()

        # feeding the html contents in the
        # HTMLTableParser object
        p.feed(xhtml)

        # Now finally obtaining the data of
        # the table required
        #pprint(p.tables[1])

        df_testing = pd.DataFrame(p.tables[1])
        column_list = list(df_testing[0].values)

        away = pd.DataFrame(df_testing[1]).T
        away.columns = column_list
        away = away.reset_index()
        # away = away.drop(columns = ['index', 'Matchup'])
        away = away.drop(columns = ['index'])
        #away.drop(away.columns[[13]], axis=1, inplace=True)
        away = away.rename(columns = {'1st Downs': 'first_downs_away',
                                    # 'Passing 1st downs': 'first_downs_passing_away',
                                    # 'Rushing 1st downs': 'first_downs_rushing_away', 
                                    # '1st downs from penalties': 'first_down_by_penalty_away', 
                                    '3rd down efficiency': 'third_down_away', 
                                    '4th down efficiency': 'fourth_down_away', 
                                    # 'Total Plays': 'total_plays_away', 
                                    'Total Yards': 'total_yards_away', 
                                    # 'Total Drives': 'total_drives_away', 
                                    # 'Yards per Play': 'yards_per_play_away', 
                                    'Passing': 'passing_away', 
                                    'Comp-Att': 'comp_att_away', 
                                    'Yards per pass': 'yards_per_pass_away',  
                                    # 'Sacks-Yards Lost': 'sack_yards_lost_away', 
                                    'Rushing': 'rushing_away', 
                                    'Rushing Attempts': 'rushing_att_away', 
                                    'Yards per rush': 'yards_per_rush_away', 
                                    # 'Red Zone (Made-Att)': 'red_zone_att_away', 
                                    'Penalties': 'penalty_away', 
                                    'Turnovers': 'turnovers_away', 
                                    'Interceptions thrown': 'int_thrown_away',
                                    'Fumbles lost': 'fumbles_lost_away',
                                    # 'Rushing 1st downs': 'first_down_rushing_away', 
                                    # 'Defensive / Special Teams TDs': 'defensive_td_away', 
                                    'Possession': 'possession_away'})

        home = pd.DataFrame(df_testing[2]).T
        home.columns = column_list
        home = home.reset_index()
        # home = home.drop(columns = ['index', 'Matchup'])
        home = home.drop(columns = ['index'])
        #home.drop(home.columns[[13]], axis=1, inplace=True)
        home = home.rename(columns = {'1st Downs': 'first_downs_home',
                                    # 'Passing 1st downs': 'first_downs_passing_home',
                                    # 'Rushing 1st downs': 'first_downs_rushing_home', 
                                    # '1st downs from penalties': 'first_down_by_penalty_home', 
                                    '3rd down efficiency': 'third_down_home', 
                                    '4th down efficiency': 'fourth_down_home', 
                                    # 'Total Plays': 'total_plays_home', 
                                    'Total Yards': 'total_yards_home', 
                                    # 'Total Drives': 'total_drives_home', 
                                    # 'Yards per Play': 'yards_per_play_home', 
                                    'Passing': 'passing_home', 
                                    'Comp-Att': 'comp_att_home', 
                                    'Yards per pass': 'yards_per_pass_home',  
                                    # 'Sacks-Yards Lost': 'sack_yards_lost_home', 
                                    'Rushing': 'rushing_home', 
                                    'Rushing Attempts': 'rushing_att_home', 
                                    'Yards per rush': 'yards_per_rush_home', 
                                    # 'Red Zone (Made-Att)': 'red_zone_att_home', 
                                    'Penalties': 'penalty_home', 
                                    'Turnovers': 'turnovers_home', 
                                    'Interceptions thrown': 'int_thrown_home',
                                    'Fumbles lost': 'fumbles_lost_home',
                                    # 'Rushing 1st downs': 'first_down_rushing_home', 
                                    # 'Defensive / Special Teams TDs': 'defensive_td_home', 
                                    'Possession': 'possession_home'})

        # check to see if first_downs_home is a column in game_stat_temp. I found that some games did not have stats to parse.
        if 'first_downs_home' not in home.columns:
            home = pd.DataFrame(columns = ['first_downs_home', 'third_down_home', 'fourth_down_home', 'total_yards_home', 'passing_home', 'comp_att_home', 'yards_per_pass_home', 'rushing_home', 'rushing_att_home', 'yards_per_rush_home', 'penalty_home', 'turnovers_home', 'int_thrown_home', 'fumbles_lost_home', 'possession_home'])
            away = pd.DataFrame(columns = ['first_downs_away', 'third_down_away', 'fourth_down_away', 'total_yards_away', 'passing_away', 'comp_att_away', 'yards_per_pass_away', 'rushing_away', 'rushing_att_away', 'yards_per_rush_away', 'penalty_away', 'turnovers_away', 'int_thrown_away', 'fumbles_lost_away', 'possession_away'])
            game_stat_temp = pd.concat([away, home], axis=1)

            # insert a 0 for all columns in the first row
            game_stat_temp.loc[0] = 0
            game_stat_temp_col_reorder = ['first_downs_away', 'third_down_away', 'fourth_down_away', 'total_yards_away', 'passing_away', 'comp_att_away', 'yards_per_pass_away', 'rushing_away', 'rushing_att_away', 'yards_per_rush_away', 'penalty_away', 'turnovers_away', 'int_thrown_away', 'fumbles_lost_away', 'possession_away'
                                          , 'first_downs_home', 'third_down_home', 'fourth_down_home', 'total_yards_home', 'passing_home', 'comp_att_home', 'yards_per_pass_home', 'rushing_home', 'rushing_att_home', 'yards_per_rush_home', 'penalty_home', 'turnovers_home', 'int_thrown_home', 'fumbles_lost_home', 'possession_home']
            
            game_stat_temp = game_stat_temp[game_stat_temp_col_reorder]

            # ensure we have no duplicate columns
            game_stat_temp = game_stat_temp.loc[:,~game_stat_temp.columns.duplicated()]
        else:
            game_stat_temp = pd.concat([away, home], axis=1)
            game_stat_temp_col_reorder = ['first_downs_away', 'third_down_away', 'fourth_down_away', 'total_yards_away', 'passing_away', 'comp_att_away', 'yards_per_pass_away', 'rushing_away', 'rushing_att_away', 'yards_per_rush_away', 'penalty_away', 'turnovers_away', 'int_thrown_away', 'fumbles_lost_away', 'possession_away'
                                          , 'first_downs_home', 'third_down_home', 'fourth_down_home', 'total_yards_home', 'passing_home', 'comp_att_home', 'yards_per_pass_home', 'rushing_home', 'rushing_att_home', 'yards_per_rush_home', 'penalty_home', 'turnovers_home', 'int_thrown_home', 'fumbles_lost_home', 'possession_home']
            
            game_stat_temp = game_stat_temp[game_stat_temp_col_reorder]

            # ensure we have no duplicate columns
            game_stat_temp = game_stat_temp.loc[:,~game_stat_temp.columns.duplicated()]

        # print(game_stat_temp)

        return game_stat_temp

    except Exception as e:
        print(e)
        print('Error in parsing game stats for: ', url)
        home = pd.DataFrame(columns = ['first_downs_home', 'third_down_home', 'fourth_down_home', 'total_yards_home', 'passing_home', 'comp_att_home', 'yards_per_pass_home', 'rushing_home', 'rushing_att_home', 'yards_per_rush_home', 'penalty_home', 'turnovers_home', 'int_thrown_home', 'fumbles_lost_home', 'possession_home'])
        away = pd.DataFrame(columns = ['first_downs_away', 'third_down_away', 'fourth_down_away', 'total_yards_away', 'passing_away', 'comp_att_away', 'yards_per_pass_away', 'rushing_away', 'rushing_att_away', 'yards_per_rush_away', 'penalty_away', 'turnovers_away', 'int_thrown_away', 'fumbles_lost_away', 'possession_away'])
        game_stat_temp = pd.concat([away, home], axis=1)

        # insert a 0 for all columns in the first row
        game_stat_temp.loc[0] = 0

        game_stat_temp_col_reorder = ['first_downs_away', 'third_down_away', 'fourth_down_away', 'total_yards_away', 'passing_away', 'comp_att_away', 'yards_per_pass_away', 'rushing_away', 'rushing_att_away', 'yards_per_rush_away', 'penalty_away', 'turnovers_away', 'int_thrown_away', 'fumbles_lost_away', 'possession_away'
                                          , 'first_downs_home', 'third_down_home', 'fourth_down_home', 'total_yards_home', 'passing_home', 'comp_att_home', 'yards_per_pass_home', 'rushing_home', 'rushing_att_home', 'yards_per_rush_home', 'penalty_home', 'turnovers_home', 'int_thrown_home', 'fumbles_lost_home', 'possession_home']
            
        game_stat_temp = game_stat_temp[game_stat_temp_col_reorder]

        # ensure we have no duplicate columns
        game_stat_temp = game_stat_temp.loc[:,~game_stat_temp.columns.duplicated()]

        return game_stat_temp