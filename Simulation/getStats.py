from pybaseball import statcast_batter, statcast_single_game, statcast_pitcher

import pandas as pd
import pickle

with open('pitchersgamesdict.pickle', 'rb') as f:
    pitchergamesdict = pickle.load(f)

def outcome(desc):
     if desc == 'hit_into_play':
          return 1
     else:
          return 0


def getBattingAverage(batter: int, count: list, pitch_type: str, start: str,
                      end: str):
     print('in function')
     bats = statcast_batter(start, end, batter)
     bats['outcome'] = bats['description'].apply(outcome)
     return_list = []
     bats = bats[bats['strikes'] == count[0]]
     bats = bats[bats['balls'] == count[1]]
     bats = bats[bats['outs_when_up'] == count[2]]

     return bats.groupby('pitch_type').mean()['outcome'][pitch_type]





def getBatterStats(batter: int, pitch_types: list, start: str, end: str):

    full_bats = statcast_batter(start, end, batter)
    strikes = 0
    balls = 0
    fouls = 0
    singles = 0
    doubles = 0
    triples = 0
    home_runs = 0
    hbp = 0
    pitches = 0
    for pitch in pitch_types:
        bats = full_bats[full_bats['pitch_type'] == pitch]
        bats.dropna(subset='type',inplace=True)
        strikes += int(bats['type'].value_counts()['S'])
        balls += int(bats['type'].value_counts()['B'])
        fouls += int(bats['description'].value_counts()['foul'])
        try:
            singles += int(bats['events'].value_counts()['single'])
        except:
            pass
        try:
            doubles += int(bats['events'].value_counts()['double'])
        except:
            pass
        try:
            triples += int(bats['events'].value_counts()['triple'])
        except:
            pass
        try:
            home_runs += int(bats['events'].value_counts()['home_run'])
        except:
            pass
        try:
            hbp += int(bats['events'].value_counts()['hit_by_pitch'])
        except:
            pass


        pitches += len(bats)

    return_list = [
     strikes, balls, fouls, singles, doubles, triples, home_runs, hbp
     ]
    return_list = [a / pitches for a in return_list]
    return {batter: return_list}




def fieldOutProb(pitcher, start, end):
     try:
        games_dict = pitchergamesdict[pitcher]
     except:
        games_dict = pitchergamesdict[621345]
        
     try:
          df = pd.concat(games_dict.values(), ignore_index=True)
          total_hits = 0
          total_field_outs = 0
          for i, row in df.iterrows():
               if row['description'] == 'hit_into_play':
                    total_hits += 1
               if row['events'] == 'field_out':
                    total_field_outs += 1

          return total_field_outs / total_hits
     except:
          return 0.80
