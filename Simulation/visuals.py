import copy
import scalePitch
import matplotlib.pyplot as plt


def createPitchChart(DF):
  df = copy.deepcopy(DF)
  ball_r = 1.43 / 12
  sz_right = 8.5 / 12
  sz_left = -8.5 / 12

  top_avg = df.sz_top.mean()
  bot_avg = df.sz_bot.mean()

  df['scaled_y'] = df.apply(
    lambda X: scalePitch.scalePitch(top_avg, bot_avg, sz_left, sz_right, X.
                                    sz_top, X.sz_bot, X.plate_x, X.plate_z),
    axis=1)

  ball_X = list(df['plate_x'])
  ball_Y = list(df['scaled_y'])
  strikes = df[df['isStrike'] == True]
  balls = df[df['isStrike'] == False]

  fig, ax = plt.subplots()
  for i, row in strikes.iterrows():
    if row['isMissedCall']:
      ax.scatter(ball_X[i], ball_Y[i], s=1.43 * 72, c='purple', alpha=0.5)
    else:
      ax.scatter(ball_X[i], ball_Y[i], s=1.43 * 72, c='green', alpha=0.5)
  for i, row in balls.iterrows():
    if row['isMissedCall']:
      ax.scatter(ball_X[i], ball_Y[i], s=1.43 * 72, c='purple', alpha=0.5)
    else:
      ax.scatter(ball_X[i], ball_Y[i], s=1.43 * 72, c='red', alpha=0.5)

  fig.set_size_inches(10.5, 10.5)
  strike_zone = plt.Rectangle((sz_left, bot_avg),
                              sz_right - sz_left, (top_avg) - (bot_avg),
                              edgecolor='black',
                              facecolor='none',
                              linewidth=2)
  ax.add_patch(strike_zone)

  ax.set_xlim([-4, 4])
  ax.set_ylim([-2, 6])

  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  plt.show()
