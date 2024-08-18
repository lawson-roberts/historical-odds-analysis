# historical-odds-analysis

## Table of Contents

- [Introduction](#introduction)
- [Files](#files)
- [Data Used](#data-used)
- [Model Feature Ideas](#model-feature-ideas)

## Introduction

There is a streamlit app I have been working on found here [NCAA Odds Outcome Predictions](https://ncaa-odds-predictions.streamlit.app/). At the moment we have 3 models.

- Money Line Classification: this will predict a 1 if the model thinks the home team will win from a money line perspective aka just winning the game outright.

One thing to call out for Spread classification models. I created two seperate models here because sometimes the home vs away spread points you are calculating your target based off of are different.

- Home Team Spread Classification: this will preduct a 1 if the model thinkgs the home team will beat the home team spread points from our odds data source.
- Away Team Spread Classification: this will preduct a 1 if the model thinkgs the away team will beat the home team spread points from our odds data source.

Personally I found this confusing so here was an example explained that I found helpful...

- Point Spread:
  - Away Point Spread: +27.5
  - Home Point Spread: -27.5

The point spread is used to even the playing field between two teams, especially when one team is much stronger than the other. In this example:

- Away team is given +27.5 points. This means the away team can lose by up to 27 points and still "cover the spread." If they lose by 28 points or more, you lose the bet.
- Home team is given -27.5 points. This means the home team must win by at least 28 points to "cover the spread." If they win by 27 points or less, or lose, you lose the bet.

- Spread Line:
  - Both spreads have a line of -112.

The spread line (or odds) indicates how much you need to risk to win $100. The negative number means you must bet that amount to win $100.

- A -112 line means you need to bet $112 to win $100. If you win, you get your $112 back plus $100 in winnings, totaling $212.
- If the line were positive (e.g., +112), you would bet $100 to win $112.

- Summary:
  - If you bet on the away team at +27.5 and they lose by 27 points or fewer (or win outright), you win your bet.
  - If you bet on the home team at -27.5, they need to win by at least 28 points for you to win.
  - In either case, you're risking $112 to win $100, as indicated by the -112 spread line.

## Files

- ![NCAA Stats Crawling](ncaa_stats_crawler.ipynb) - looking into this to see how we could include historical game statistics into the mode. This does increase model performance but the challenge here is getting accurate inputs at the time of prediction.
- ![NCAA Odds Crawling](ncaa_odds_crawler.ipynb) - will likely use this going forward in order to show all odds for games happening within a given week. Currently the API we use only defaults to the Top 25 games of the week according to ESPN so this is limiting what the app could cover.
- ![Team Name Normilization](team_normalization.ipynb) - Needed this to take the historical odds file and match these teams up with the team names from ESPN data in order to combine this data. The goal here will be to assign a game id to reach record in the odds dataset.

## Data Used

- Using data collected from [Scott Free LLC](https://www.scottfreellc.com/shop/p/historical-odds-sample-data) to start.
- Will likely need to scrape our own Odds data to keep this updated weekly.
  - Give ESPN a shot. Might be able to get this info from the Caesars API similar to the NFL odds.
    - [This looks promising](https://www.espn.com/college-football/odds)
- Could be interesting to add team stats into the picture as well

## Model Feature Ideas

- Odds Data Only
  - Easy one would be to add if the team was home or away
  - Win Streak
- Stats Data Included
  - make this player specific?
  - would need to find a place to scrape game stats for college anyway. Maybe we could give ESPN a try again similar to NFL stats?
