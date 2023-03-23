import copy


def inStrikeZone(ball_x, ball_y, ball_radius, sz_left, sz_right, sz_top,
                 sz_bot):
  """
 _______
|/ ___ \|
|	|		|	|
|	|		|	|
|\ --- /|
 -------
Check within "strike zone + ball radius" and subtract instances in corners
"""

  zeroed_sz_top = (sz_top - sz_bot) / 2
  zeroed_sz_bot = (sz_bot - sz_top) / 2
  zeroed_ball_y = ball_y - (sz_top + sz_bot) / 2

  if (ball_x <= (sz_right + ball_radius) and ball_x >= (sz_left - ball_radius)
      and ball_y <= (sz_top + ball_radius) and ball_y >=
      (sz_bot - ball_radius)):

    if (abs(ball_x) > sz_right and abs(zeroed_ball_y) > zeroed_sz_top
        and (((abs(ball_x) - sz_right)**2 +
              (abs(zeroed_ball_y) - zeroed_sz_top)**2)**0.5) > ball_radius):
      return False
    else:
      return True

  return False


def is_in_strike_zone(ball_center_x, ball_center_y, ball_radius,
                      strike_zone_left, strike_zone_right, strike_zone_top,
                      strike_zone_bottom):
  if (ball_center_x >= strike_zone_left and ball_center_x <= strike_zone_right
      and ball_center_y <= strike_zone_top
      and ball_center_y >= strike_zone_bottom):
    return True
  if (ball_center_x < strike_zone_left):
    closest_x = strike_zone_left
  elif (ball_center_x > strike_zone_right):
    closest_x = strike_zone_right
  else:
    closest_x = ball_center_x

  if (ball_center_y > strike_zone_top):
    closest_y = strike_zone_top
  elif (ball_center_y < strike_zone_bottom):
    closest_y = strike_zone_bottom
  else:
    closest_y = ball_center_y

  distance = ((ball_center_x - closest_x)**2 +
              (ball_center_y - closest_y)**2)**0.5
  if distance <= ball_radius:
    return True

  return False


def detectMissedCalls(df):
  df = copy.deepcopy(df)
  df['isMissedCall'] = 0
  missed_calls = []
  for i, row in df.iterrows():
    if row['isStrike'] == True:
      if row['description'] == 'ball':
        missed_calls.append(1)
      else:
        missed_calls.append(0)
    else:
      if row['description'] == 'called_strike':
        missed_calls.append(1)
      else:
        missed_calls.append(0)
  print(len(missed_calls))
  df['isMissedCall'] = missed_calls
  return df
