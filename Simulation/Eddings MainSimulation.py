#Imports
import detect as detectStrike
import scalePitch
import fieldOutBaseState
import atBat
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import pickle
from pybaseball import playerid_reverse_lookup
import visuals
import copy
import getStats
from tqdm import tqdm
pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)


result_dicts = {}
ball_r = 1.43 / 12
sz_right = 8.5 / 12
sz_left = -8.5 / 12
df = pd.read_csv("/Group A/Eddings 6-21-22/TOR at CWS 6-21-22.csv")
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
with open('hoberg.pickle', 'rb') as f:
	hoberg_weights = pickle.load(f)

#Detect Strike or Ball and Missed Calls
df['isStrike'] = df.apply(lambda x: detectStrike.inStrikeZone(
    x.plate_x, x.plate_z, ball_r, sz_left, sz_right, x.sz_top, x.sz_bot),
                          axis=1)
df = detectStrike.detectMissedCalls(df)
#visuals.createPitchChart(df)


#Get Missed Call Indices
missed_call_indexes = []
for i, row in df.iterrows():
    if row['isMissedCall'] == 1:
        missed_call_indexes.append(i)

#Get beginning of half inning indices
half_innings = [0]
for i, row in df.iterrows():
    if i > 1:
        if row['inning_topbot'] != df['inning_topbot'][i - 1]:
            half_innings.append(i)
#track game outcomes
game_outcomes= {}
initial_runs = []
all_pitches_made = []
#Get Outcome for Each In Missed Call Index
for iteration in tqdm(range(100)):
    for start_index in tqdm(reversed(missed_call_indexes)):
        i = start_index
        current_df = copy.deepcopy(df).iloc[:i+2]
        outs = current_df.outs_when_up[i]
        runs = {
                "home": df.home_score[i],
                "away": df.away_score[i]
            }
        
        # sim to end of the game from index i
        
        if (i == start_index):
            if df['description'][i] =='ball':
                df['balls'][i+1] -=1
                df['strikes'][i+1] +=1
                if df['strikes'][i+1] ==3:
                    outs+=1
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                    
                    
        i+=1        
        
        if outs<3:
            if current_df.inning_topbot[i] == "Top":
                gamestate = 'away'
            else:
                gamestate = 'home'  
            if current_df.inning_topbot[i] == 'Top':
                half_inning_index = current_df.inning[i]*2-2
            elif current_df.inning_topbot[i] == 'Bot': 
                half_inning_index = current_df.inning[i]*2-1
        else:
            if current_df.inning_topbot[i] == "Top":
                gamestate = 'home'
            else:
                gamestate = 'away'  
            if current_df.inning_topbot[i] == 'Top':
                half_inning_index = current_df.inning[i]*2-1
            elif current_df.inning_topbot[i] == 'Bot': 
                half_inning_index = current_df.inning[i]*2
                

        while True:
            #home first away second
        
            # detect which half-inning
        
            batter = current_df.batter[i]
            pitcher = current_df.pitcher[i]
            strikes = current_df.strikes[i]
            balls = current_df.balls[i]
            try:
                previous_pitch = current_df.pitch_type[i-1]
            except:
                previous_pitch= pitch_type
            stand = current_df.stand[i]
            pitch_num = current_df.pitch_number[i]
            if i == start_index+1:
                base_state = (pd.notna(current_df.on_3b[i]) * 100 + pd.notna(current_df.on_2b[i]) * 10 +
                        pd.notna(current_df.on_1b[i]) * 1)
            else:
                base_state = 0
            #While in half inning
            while outs < 3:
                pitches_made =0
                result,pitches_made, pitch_type = atBat.atBat(balls, strikes, batter, pitcher, previous_pitch, stand, eddings_weights, pitch_num)
                if result == "Strikeout":
                    outs += 1
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                elif result == "Single":
                    weights=[getStats.fieldOutProb(current_df.pitcher[i], '2021-03-20', '2022-03-20'), 1 - getStats.fieldOutProb(current_df.pitcher[i], '2021-03-20', '2022-03-20')]
                    fieldOut = random.choices([1, 0], weights=weights, k=1)[0]
                    if fieldOut == 1:
                        base_state = fieldOutBaseState.fieldOutBaseState(base_state, batter)[0]
                        outs += 1
                        if base_state == 1:
                            base_state = 11
                        elif base_state == 10:
                            base_state = 101
                        elif base_state == 100:
                            runs[gamestate] += 1
                            base_state = 1
                        elif base_state == 11:
                            base_state == 111
                        elif base_state == 110:
                            runs[gamestate] += 1
                            base_state = 101
                        elif base_state == 101:
                            runs[gamestate] += 1
                            base_state = 11
                        elif base_state == 111:
                            runs[gamestate] += 1
                            base_state = 111
                        elif base_state == 0:
                            base_state = 1
                    elif fieldOut == 0:
                        if base_state == 1:
                            base_state = 11
                        elif base_state == 10:
                            base_state = 101
                        elif base_state == 100:
                            runs[gamestate] += 1
                            base_state = 1
                        elif base_state == 11:
                            base_state == 111
                        elif base_state == 110:
                            runs[gamestate] += 1
                            base_state = 101
                        elif base_state == 101:
                            runs[gamestate] += 1
                            base_state = 11
                        elif base_state == 111:
                            runs[gamestate] += 1
                            base_state = 111
                        elif base_state == 0:
                            base_state = 1
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                elif result == "Double":
                    weights=[getStats.fieldOutProb(current_df.pitcher[i], '2021-03-20', '2022-03-20'), 1 - getStats.fieldOutProb(current_df.pitcher[i], '2021-03-20', '2022-03-20')]
                    fieldOut = random.choices([1, 0], weights=weights, k=1)[0]
                    if fieldOut == 1:
                        base_state = fieldOutBaseState.fieldOutBaseState(base_state, batter)[0]
                        outs += 1
                        if base_state == 1:
                            base_state = 110
                        elif base_state == 10:
                            runs[gamestate]+=1
                            base_state = 10
                        elif base_state == 100:
                            runs[gamestate] += 1
                            base_state = 10
                        elif base_state == 11:
                            runs[gamestate] += 1
                            base_state == 110
                        elif base_state == 110:
                            runs[gamestate] += 2
                            base_state = 10
                        elif base_state == 101:
                            runs[gamestate] += 1
                            base_state = 110
                        elif base_state == 111:
                            runs[gamestate] += 2
                            base_state = 110
                        elif base_state == 0:
                            base_state = 10
                    elif fieldOut == 0:
                        if base_state == 1:
                            base_state = 110
                        elif base_state == 10:
                            runs[gamestate]+=1
                            base_state = 10
                        elif base_state == 100:
                            runs[gamestate] += 1
                            base_state = 10
                        elif base_state == 11:
                            runs[gamestate] += 1
                            base_state == 110
                        elif base_state == 110:
                            runs[gamestate] += 2
                            base_state = 10
                        elif base_state == 101:
                            runs[gamestate] += 1
                            base_state = 110
                        elif base_state == 111:
                            runs[gamestate] += 2
                            base_state = 110
                        elif base_state == 0:
                            base_state = 10
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                elif result == "Triple":
                    weights=[getStats.fieldOutProb(current_df.pitcher[i], '2021-03-20', '2022-03-20'), 1 - getStats.fieldOutProb(current_df.pitcher[i], '2021-03-20', '2022-03-20')]
                    fieldOut = random.choices([1, 0], weights=weights, k=1)[0]
                    if fieldOut == 1:
                        base_state = fieldOutBaseState.fieldOutBaseState(base_state, batter)[0]
                        outs += 1
                        if base_state == 1:
                            runs[gamestate] += 1
                            base_state = 100
                        elif base_state == 10:
                            runs[gamestate]+=1
                            base_state = 100
                        elif base_state == 100:
                            runs[gamestate] += 1
                            base_state = 100
                        elif base_state == 11:
                            runs[gamestate] += 2
                            base_state == 100
                        elif base_state == 110:
                            runs[gamestate] += 2
                            base_state = 100
                        elif base_state == 101:
                            runs[gamestate] += 2
                            base_state = 100
                        elif base_state == 111:
                            runs[gamestate] += 3
                            base_state = 100
                        elif base_state == 0:
                            base_state = 100
                    elif fieldOut == 0:
                        if base_state == 1:
                            runs[gamestate] += 1
                            base_state = 100
                        elif base_state == 10:
                            runs[gamestate]+=1
                            base_state = 100
                        elif base_state == 100:
                            runs[gamestate] += 1
                            base_state = 100
                        elif base_state == 11:
                            runs[gamestate] += 2
                            base_state == 100
                        elif base_state == 110:
                            runs[gamestate] += 2
                            base_state = 100
                        elif base_state == 101:
                            runs[gamestate] += 2
                            base_state = 100
                        elif base_state == 111:
                            runs[gamestate] += 3
                            base_state = 100
                        elif base_state == 0:
                            base_state = 100
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                elif result == "HR":
                    
                    
                    runs[gamestate] += str(base_state).count('1') + 1
                    
                    base_state = 0
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                elif result == "Walk" or "HBP":
                    #still getting two runs from a walk
                    temp_base_state = base_state
                    if base_state==1 or base_state ==101:
                        #make seperate cases
                        base_state += 10
                    elif base_state == 111:
                        base_state = ((base_state % 100) * 10) + 1
                        runs[gamestate] += 1
                    elif base_state == 11 or base_state == 1:
                        base_state = ((base_state % 100) * 10) + 1
                    elif base_state == 100 or base_state == 110 or base_state == 0:
                        base_state+=1
                        
                    try:
                        batter = eddings_batting_order[gamestate][
                            eddings_batting_order[gamestate].index(batter) + 1]
                    except:
                        batter = eddings_batting_order[gamestate][0]
                i += pitches_made
                current_df.loc[i] = [0 for i in range(len(current_df.columns))]
                current_df.at[i, 'batter'] = batter
                current_df.at[i, 'pitcher'] = pitcher
                current_df.at[i, 'events'] = result
                current_df.at[i, 'away_score'] = runs['away']
                current_df.at[i, 'home_score'] = runs['home']
                current_df.at[i,'inning'] = int((half_inning_index+2)/2)
                
                
                
                
                    
                    
            
            
            #There is a switch in half inning
            
            outs = 0
            if gamestate == 'home':
                gamestate = 'away'
            else: 
                gamestate = 'home'
            
            
            half_inning_index+=1
            if half_inning_index >= 16 and runs['away']!=runs['home'] and (half_inning_index % 2 !=0):
                result_dicts[start_index] = current_df
                break
            else:
                pass



            
        