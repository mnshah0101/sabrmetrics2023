#Imports
import detect as detectStrike
import scalePitch
import fieldOutBaseState
import getStats
#import atBat
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import pickle
from pybaseball import playerid_reverse_lookup
import visuals


ball_r = 1.43 / 12
sz_right = 8.5 / 12
sz_left = -8.5 / 12
df = pd.read_csv("Group A/Eddings 6-21-22/TOR at CWS 6-21-22.csv")
eddings_batting_order = {}
eddings_batting_order['away'] = [
    543807, 666182, 665489, 672386, 606192, 669289, 656305, 666971, 606132
]
eddings_batting_order['home'] = [
    641313, 683734, 673357, 547989, 572041, 641553, 664874, 543281, 664901
]

hoberg_batting_order = {}

#Constants and df
with open('eddings.pickle', 'rb') as f:
	eddings_weights = pickle.load(f)

#Detect Strike or Ball and Missed Calls
df['isStrike'] = df.apply(lambda x: detectStrike.is_in_strike_zone(
    x.plate_x, x.plate_z, ball_r, sz_left, sz_right, x.sz_top, x.sz_bot),
                          axis=1)
df = detectStrike.detectMissedCalls(df)
visuals.createPitchChart(df)

#Get Missed Call Indices
missed_call_index = []
for i, row in df.iterrows():
    if row['isMissedCall'] == 1:
        missed_call_index.append(i)

#Get half inning indices
half_innings = [0]
for i, row in df.iterrows():
    if i > 1:
        if row['inning_topbot'] != df['inning_topbot'][i - 1]:
            half_innings.append(i)

print(half_innings)
game_outcomes= {}
for i in reversed(missed_call_indexes):
  outs = df.outs_when_up[i]
  runs = {
            "home": df.home_score[i],
            "away": df.away_score[i]
        } 
  isOver = False
    # sim to end of the game
    while not isOver:
        #home first away second
        if df.inning_topbot == "Top":
            gamestate = 'away'
        else:
            gamestate = 'home'
    
        # detect which half-inning
        if df.inning_topbot[i] == 'Top':
            half_inning_index = half_innings[df.inning[i]*2-2]
        elif df.inning_topbot[i] == 'Bot': 
            half_inning_index = half_innings[df.inning[i]*2-1]

        batter = df.batter[i]
        pitcher = df.pitcher[i]
        strikes = df.strikes[i]
        balls = df.balls[i]
        previous_pitch = df.pitch_type[i-1]
        stand = df.stand[i]
        pitch_num = df.pitch_num[i]
        
        base_state = (pd.notna(df.on_3b[i]) * 100 + pd.notna(df.on_2b[i]) * 10 +
                      pd.notna(df.on_1b[i]) * 1)
        while outs < 3:
            result = atBat(balls, strikes, batter, pitcher, previous_pitch, stand, eddings_weights, pitch_num)
            if result == "Strikeout":
                outs += 1
                batter = eddings_batting_order[gamestate][
                    eddings_batting_order[gamestate].index(batter) + 1]
            elif result == "Single":
                if random.choices(
                    [1, 0],
                        weights=[
                            fieldOutProb(df.pitcher[i], '2021-03-20',
                                         '2022-03-20'), 1 -
                            fieldOutProb(df.pitcher[i], '2021-03-20', '2022-03-20')
                        ],
                        k=1) == [1]:
                    temp_base_state = fieldOutBaseState(base_state)
                    outs += 1
                base_state = ((base_state % 100) * 10) + 1
                runs[gamestate] += str(temp_base_state).count('1') + 1 - str(
                    base_state).count('1')
                batter = eddings_batting_order[gamestate][
                    eddings_batting_order[gamestate].index(batter) + 1]
            elif result == "Double":
                if random.choices(
                    [1, 0],
                        weights=[
                            fieldOutProb(df.pitcher[i], '2021-03-20',
                                         '2022-03-20'), 1 -
                            fieldOutProb(df.pitcher[i], '2021-03-20', '2022-03-20')
                        ],
                        k=1) == [1]:
                    temp_base_state = fieldOutBaseState(base_state)
                    outs += 1
                base_state = ((base_state % 10) * 100) + 10
                runs[gamestate] += str(temp_base_state).count('1') + 1 - str(
                    base_state).count('1')
                batter = eddings_batting_order[gamestate][
                    eddings_batting_order[gamestate].index(batter) + 1]
            elif result == "Triple":
                if random.choices(
                    [1, 0],
                        weights=[
                            fieldOutProb(df.pitcher[i], '2021-03-20',
                                         '2022-03-20'), 1 -
                            fieldOutProb(df.pitcher[i], '2021-03-20', '2022-03-20')
                        ],
                        k=1) == [1]:
                    temp_base_state = fieldOutBaseState(base_state)
                    outs += 1
                base_state = ((base_state % 1) * 1000) + 100
                runs[gamestate] += str(temp_base_state).count('1') + 1 - str(
                    base_state).count('1')
                batter = eddings_batting_order[gamestate][
                    eddings_batting_order[gamestate].index(batter) + 1]
            elif result == "HR":
                temp_base_state = base_state
                base_state = 000
                runs[gamestate] += str(temp_base_state).count('1') + 1 - str(
                    base_state).count('1')
                batter = eddings_batting_order[gamestate][
                    eddings_batting_order[gamestate].index(batter) + 1]
            elif result == "Walk" or "HBP":
                temp_base_state = base_state
                base_state = ((base_state % 100) * 10) + 1
                runs[gamestate] += str(temp_base_state).count('1') + 1 - str(
                    base_state).count('1')
                batter = eddings_batting_order[gamestate][
                    eddings_batting_order[gamestate].index(batter) + 1]
        if batter == df.batter[half_innings[half_inning_index+1]-1] && df.(gamestate + str(_score)) == runs[gamestate]
            i = missed_call_indexes[i+1]
        else:
            outs = 0
            if gamestate == 'home':
                gamestate = 'away'
            else: 
                gamestate = 'home'