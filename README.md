# historical-odds-analysis

## Table of Contents

- [Introduction](#introduction)
- [Files](#files)
- [Data Used](#data-used)
- [Model Feature Ideas](#model-feature-ideas)

## Introduction

## Files

- ![NCAA Stats Crawling](ncaa_stats_crawler.ipynb) -
- ![NCAA Odds Crawling](ncaa_odds_crawler.ipynb) -
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
