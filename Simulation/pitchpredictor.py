#imports
import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
with open('fastball_pitch_model.sav', 'rb') as f:
  fb_model = pickle.load(f)


#functions:
def LorR(stand):
  if stand == 'R':
    return 0
  else:
    return 1


def pitch_type(pitch):
  #fastballs
  if pitch in ['FF', 'FC', "FT", 'FA', 'SI', 'SF']:
    return 0

  #changeups
  elif pitch in ["FS", 'CH', 'KC']:
    return 1
  #curveballs
  elif pitch in ['CB', "CU", "KN"]:
    return 2

  #sliders
  elif pitch == 'SL':
    return 3
  else:
    return None


def isFastBall(pitch):
  #fastballs
  if (type(pitch) == str):
    if pitch in ['FF', 'FC', "FT", 'FA', 'SI', 'SF']:
      return 0
    else:
      return 1
  else:
    if pitch == 0:
      return 0
    else:
      return 1


def on_3b(b):
  if pd.isna(b):
    return 0
  else:
    return b


def count(balls, strikes):
  return "{ball}-{strike}".format(ball=balls, strike=strikes)


def cat_count(count):
  if count == '0-0':
    return 0
  elif count == '0-1':
    return 1
  elif count == '0-2':
    return 2
  elif count == '1-0':
    return 3
  elif count == '1-1':
    return 4
  elif count == '1-2':
    return 5
  elif count == '2-0':
    return 6
  elif count == '2-1':
    return 7
  elif count == '2-2':
    return 8
  elif count == '3-0':
    return 9
  elif count == '3-1':
    return 10
  elif count == '3-2':
    return 11


with open('nonfastball_pitch_model.sav', 'rb') as f:
  nfb_model = pickle.load(f)
with open('pitcherencoder.sav', 'rb') as f:
  pitchencoder = pickle.load(f)


def getFastBallWeights(pitcher, prev_pitch, pitch_num, count_list, stand):
  """
  pitcherID - int
  prev_pitch: pitch type as a string or int(cat)
  pitch_num
  count: [balls,strikes]
  stand: L or R
  returns: probs of fastball or nonfastball
  """
  pitcher_input = pitchencoder.transform([pitcher])
  if (type(prev_pitch) == str):
    prev_pitch_input = pitch_type(prev_pitch)
  else:
    prev_pitch_input = prev_pitch

  prev_fast_ball_input = isFastBall(prev_pitch)
  pitch_num_input = pitch_num
  cat_count_input = count(count_list[0], count_list[1])
  count_input = cat_count(cat_count_input)
  stand_input = LorR(stand)
  inputs_list = np.array([
    *pitcher_input, prev_pitch_input, pitch_num_input, count_input,
    stand_input, prev_fast_ball_input
  ])
  return fb_model.predict_proba(inputs_list.reshape(1, -1))


def getNonFastBallWeights(pitcher, prev_pitch, pitch_num, count_list, stand):
  """
  pitcherID - int
  prev_pitch: pitch type as a string or int(cat)
  pitch_num
  count: [balls,strikes]
  stand: L or R
  returns probs of CH (Changeup),CB (Curveball),SL (Slider)
  """
  pitcher_input = pitchencoder.transform([pitcher])
  if (type(prev_pitch) == str):
    prev_pitch_input = pitch_type(prev_pitch)
  else:
    prev_pitch_input = prev_pitch

  prev_fast_ball_input = isFastBall(prev_pitch)
  pitch_num_input = pitch_num
  cat_count_input = count(count_list[0], count_list[1])
  count_input = cat_count(cat_count_input)
  stand_input = LorR(stand)
  inputs_list = np.array([
    *pitcher_input, prev_pitch_input, pitch_num_input, count_input,
    stand_input, prev_fast_ball_input
  ])
  return nfb_model.predict_proba(inputs_list.reshape(1, -1))


print(getFastBallWeights(605182, "FF", 2, [0, 1], "R"))
