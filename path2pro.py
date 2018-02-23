"""
Path2Pro
This code is used to organize data from daily tournaments
""" 
import numpy as np
import pandas as pd 
import gspread_pandas as gp
from oauth2client.service_account import ServiceAccountCredentials
from gspread_pandas import Spread
from collections import OrderedDict

tournament = Spread('league','Path2Pro League (Season 1)')
tournament.sheets

### pull tournament data into dataframes
### PLAYER NAMES
tournament.open_sheet(5)
tournament
players = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER HASHTAGS
tournament.open_sheet(6)
tournament
hashtags = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER TROPHIES
tournament.open_sheet(7)
tournament
trophies = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER CLANS
tournament.open_sheet(8)
tournament
clans = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER WINLOSS
tournament.open_sheet(9)
tournament
winloss = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER GAMES
tournament.open_sheet(10)
tournament
games = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER PARTICIPATION
tournament.open_sheet(11)
tournament
participation = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER PLACEMENT
tournament.open_sheet(12)
tournament
placement = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER WINS
tournament.open_sheet(13)
tournament
wins = tournament.sheet_to_df(header_rows=1, index=True)

### PLAYER LOSSES
tournament.open_sheet(14)
tournament
losses = tournament.sheet_to_df(header_rows=1, index=True)


### reshape to get dates into rows
hashtags_reshaped = pd.melt(hashtags, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Code').drop('Rank', axis = 1)

players_reshaped = pd.melt(players, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Name').drop('Rank', axis = 1)

clans_reshaped = pd.melt(clans, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Clan').drop('Rank', axis = 1)
                       
trophies_reshaped = pd.melt(trophies, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Score').drop('Rank', axis = 1)

winloss_reshaped = pd.melt(winloss, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Winloss').drop('Rank', axis = 1)
                       
games_reshaped = pd.melt(games, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Games').drop('Rank', axis = 1)
                       
participation_reshaped = pd.melt(participation, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Participation').drop('Rank', axis = 1)

placement_reshaped = pd.melt(placement, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Placement').drop('Rank', axis = 1)
                       
wins_reshaped = pd.melt(wins, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Wins').drop('Rank', axis = 1)

losses_reshaped = pd.melt(losses, id_vars = ['Rank'], 
                       value_vars = hashtags.columns, 
                       var_name = 'Date', 
                       value_name = 'Losses').drop('Rank', axis = 1)

### merge together 
merged_df = pd.DataFrame([hashtags_reshaped['Date'], pd.to_numeric(winloss_reshaped['Winloss']), pd.to_numeric(wins_reshaped['Wins']), pd.to_numeric(losses_reshaped['Losses']), pd.to_numeric(participation_reshaped['Participation']), pd.to_numeric(games_reshaped['Games']), hashtags_reshaped['Code'], players_reshaped['Name'], pd.to_numeric(placement_reshaped['Placement']), pd.to_numeric(trophies_reshaped['Score'])]).T
print(merged_df)

### group by code, name, and date; sum the scores together if multiple exist for a given code-name-date grouping
grouped_df = merged_df.groupby(['Code', 'Name', 'Date']).sum().sort_values('Score', ascending = False)
print(grouped_df)

### sum together
summed_df = merged_df.drop('Date', axis = 1) \
    .groupby(['Code', 'Name']).sum() \
    .sort_values('Score', ascending = False).reset_index()
summed_df['li'] = list(zip(summed_df.Name, summed_df.Score))
print(summed_df)

### REGISTERED USERS
tournament.open_sheet(4)
tournament
registered = tournament.sheet_to_df(header_rows=1, index=False)
registered_list = registered['CR Tag #'].tolist()
print(registered_list)

### Filter total participant by registered users 
participants_score = summed_df[summed_df['Code'].isin(registered_list)]

tournament.df_to_sheet(participants_score, sheet='Output')
print(tournament)

participants_score.info()

