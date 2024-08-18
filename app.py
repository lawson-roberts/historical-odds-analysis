import streamlit as st
import pandas as pd
import numpy as np
import base64
import csv
from PIL import Image

## web crawling packages
from pandas import json_normalize
import json
import time
from datetime import date
from datetime import datetime
import datetime

## api and model packages
import requests
import pickle
import io

##Setting Streamlit Settings
# st.set_page_config(layout="wide")

# load models from disk
ml_model_obj = pickle.load(open('models/money_line_log_reg_model.pkl', 'rb'))
home_spread_model_obj = pickle.load(open('models/home_spread_log_reg_model.pkl', 'rb'))
away_spread_model_obj = pickle.load(open('models/away_spread_log_reg_model.pkl', 'rb'))

## can add this back later once the season starts
# ## loading predictions file to show accuracy
# predictions_hist = pd.read_csv('predictions/model_prediction_file.csv')
# predictions_hist = predictions_hist.drop(columns = 'Unnamed: 0')
# game_score_hist = pd.read_csv('data/game_scores.csv')
# game_score_hist = game_score_hist.drop(columns = 'Unnamed: 0')

# predictions_hist = predictions_hist.merge(game_score_hist, on='id')
# predictions_hist['tie_check'] = np.where(predictions_hist['away_score'] ==  predictions_hist['home_score'], 'tie', 'no tie')
# predictions_hist = predictions_hist[predictions_hist['tie_check'] == 'no tie']
# predictions_hist['winner'] = np.where(predictions_hist['away_score'] >  predictions_hist['home_score'], 'away', 'home')
# predictions_hist['prediction'] = np.where(predictions_hist['away'] >  predictions_hist['home'], 'away', 'home')
# predictions_hist['pred_correct'] = np.where(predictions_hist['winner'] == predictions_hist['prediction'], 1, 0)
# predictions_hist['away'] = round(predictions_hist['away']*100, 2)
# predictions_hist['home'] = round(predictions_hist['home']*100, 2)

# model_score = round((sum(predictions_hist['pred_correct']) / len(predictions_hist))*100, 2)

st.title("NCAA Football Game Predictions")
st.write("""
        #### - Using machine learning to find best odds of winning certain sports betting wagers
        """)
st.write("""### Data Sources:""")
st.write("""1.) https://www.scottfreellc.com/shop/p/historical-odds-sample-data used for historical odds""")
st.write("""2.) Caesars Sportsbook used for vegas bets available via ESPN API""")

# st.write("""### Model Results thus far...""")
# st.write("Accuracy Score", model_score, "%")
# st.write("""#### Game Detail for past predictions...""")
# st.write(predictions_hist.astype('object'))

def get_current_games():
    url = "https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=college-football&region=us&lang=en&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America%2FNew_York"

    payload={}
    headers = {
    'Accept': 'application/json',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response_text = json.loads(response.text)

    game_df = json_normalize(response_text['sports'], ['leagues', 'events'])
    game_dict = game_df.to_dict('index')
    return game_df, game_dict

game_df, game_dict = get_current_games()

# game_df[['away','home']] = game_df.shortName.apply(lambda x: pd.Series(str(x).split("@")))
# game_df['away'] = game_df['away'].str.strip()
# game_df['home'] = game_df['home'].str.strip()
# game_df[['date','time']] = game_df.date.apply(lambda x: pd.Series(str(x).split("T")))
# game_df['time'] = game_df['time'].str[:5]
# game_df['time'] = game_df['time'].str.replace("18", "12")
# game_df['time'] = game_df['time'].str.replace("21", "03")
# game_df['time'] = game_df['time'].str.replace("01", "07")

norm1 = json_normalize(game_df['competitors'])
norm1.columns = ['away', 'home']
home_meta = json_normalize(norm1['home'])
away_meta = json_normalize(norm1['away'])
logos = pd.concat([home_meta[['logo', 'name']], away_meta[['logo', 'name']]], axis=1)
logos.columns = ['home_logo', 'home_name', 'away_logo', 'away_name']

model_ready = game_df[['id', 'name', 'odds.pointSpread.away.close.line', 'odds.awayTeamOdds.spreadOdds', 'odds.awayTeamOdds.moneyLine'
                        , 'odds.pointSpread.home.close.line', 'odds.homeTeamOdds.spreadOdds', 'odds.homeTeamOdds.moneyLine' 
                        , 'odds.total.over.close.line', 'odds.total.over.close.odds', 'odds.total.under.close.odds']]

model_ready.rename(columns={'odds.awayTeamOdds.moneyLine': 'away_money_line'
                            , 'odds.awayTeamOdds.spreadOdds': 'away_point_spread_line'
                            , 'odds.homeTeamOdds.moneyLine': 'home_money_line'
                            , 'odds.homeTeamOdds.spreadOdds': 'home_point_spread_line'
                            , 'odds.pointSpread.home.close.line': 'home_point_spread'
                            , 'odds.pointSpread.away.close.line': 'away_point_spread'
                            , 'odds.total.over.close.line': 'over_under'
                            , 'odds.total.over.close.odds': 'over_line'
                            , 'odds.total.under.close.odds': 'under_line'}, inplace=True)

model_ready.fillna(0, inplace=True)
model_ready['home_point_spread'] = pd.to_numeric(model_ready['home_point_spread'])
model_ready['away_point_spread'] = pd.to_numeric(model_ready['away_point_spread'])
model_ready['over_line'] = pd.to_numeric(model_ready['over_line'])
model_ready['under_line'] = pd.to_numeric(model_ready['under_line'])

# replace the 'o' string with nothing for over_under column and make numeric
model_ready['over_under'] = model_ready['over_under'].str.replace('o', '')
model_ready['over_under'] = pd.to_numeric(model_ready['over_under'])
model_ready.fillna(0, inplace=True)
model_ready_logo = pd.concat([model_ready, logos], axis=1)

model_ready_for_predition = model_ready.drop(columns=['id', 'name'])

## money line pred
prediction_ml = ml_model_obj.predict(model_ready_for_predition)
probabilities_ml = pd.DataFrame(ml_model_obj.predict_proba(model_ready_for_predition), columns=['away_ml', 'home_ml'])
# probabilities_ml = probabilities_ml.rename(columns = {'away': away, 'home': home})
# prediction_value_ml = prediction_ml[0]

## home spread pred
prediction_home_spread = home_spread_model_obj.predict(model_ready_for_predition)
probabilities_home_spread = pd.DataFrame(home_spread_model_obj.predict_proba(model_ready_for_predition), columns=['away_spread_home', 'home_spread_home'])
# probabilities_home_spread = probabilities_home_spread.rename(columns = {'away': away, 'home': home})
# prediction_value_home_spread = prediction_home_spread[0]

## away spread pred
prediction_away_spread = away_spread_model_obj.predict(model_ready_for_predition)
probabilities_away_spread = pd.DataFrame(away_spread_model_obj.predict_proba(model_ready_for_predition), columns=['away_spread_away', 'home_spread_away'])
# probabilities_away_spread = probabilities_away_spread.rename(columns = {'away': away, 'home': home})
# prediction_value_away_spread = prediction_away_spread[0]

model_predictions = pd.concat([model_ready_logo, probabilities_ml, probabilities_home_spread, probabilities_away_spread], axis=1)

st.write("""
        ### Additional Game and Prediction Details if you would like to take a look this way
        """)
with st.expander("Model Predictions Table - click the dropdown to take a closer look", expanded=False):
    st.write(model_predictions.astype('object'))

with st.expander("ESPN API Table - holds additional game details and all fields ESPN provides about the game", expanded=False):
    st.write(game_df.astype('object'))


st.write('### Game Predictions')
#col1, col2, col3 = st.columns(3)
col1, col2 = st.columns(2)

for ind in model_predictions.index:

    away = model_ready_logo['away_name'][ind]
    away_logo_url =  model_ready_logo['away_logo'][ind]
    away_logo_response = requests.get(away_logo_url)
    away_image_bytes = io.BytesIO(away_logo_response.content)
    away_img = Image.open(away_image_bytes)

    home = model_ready_logo['home_name'][ind]
    home_logo_url =  model_ready_logo['home_logo'][ind]
    home_logo_response = requests.get(home_logo_url)
    home_image_bytes = io.BytesIO(home_logo_response.content)
    home_img = Image.open(home_image_bytes)

    with col1:
        st.image(home_img)
        st.write("Home Team:", model_ready_logo['home_name'][ind])
        st.write("Home Team Money Line:", model_ready['home_money_line'][ind])
        st.write("Model Predicts...", round(model_predictions['home_ml'][ind]*100, 2), "% chance of winning")
        st.write("Home Team Spread Line:", model_ready['home_point_spread_line'][ind])
        st.write("Home Team Point Spread to beat:", model_ready['home_point_spread'][ind])

        ## if we were to show both models...
        st.write("Model Predicts...", round(model_predictions['home_spread_home'][ind]*100, 2), "% chance of home team covering the above spread")
        st.write("Model Predicts...", round(model_predictions['away_spread_home'][ind]*100, 2), "% chance of away team covering the above spread")
        st.write("-------------------------")

    with col2:
        st.image(away_img)
        st.write("Away Team:", model_ready_logo['away_name'][ind])
        st.write("Away Team Money Line:", model_ready['away_money_line'][ind])
        st.write("Model Predicts...", round(model_predictions['away_ml'][ind]*100, 2), "% chance of winning")
        st.write("Away Team Spread Line:", model_ready['away_point_spread_line'][ind])
        st.write("Away Team Point Spread to beat:", model_ready['away_point_spread'][ind])

        ## if we just started with using the model to predict the away spread...but sometimes they are different

        ## if we were to show both models...
        st.write("Model Predicts...", round(model_predictions['away_spread_away'][ind]*100, 2), "% chance of away team covering the above spread")
        st.write("Model Predicts...", round(model_predictions['home_spread_away'][ind]*100, 2), "% chance of home team covering the above spread")
        st.write("-------------------------")