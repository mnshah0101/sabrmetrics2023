def scalePitch(top_avg, bot_avg, sz_left, sz_right, sz_top, sz_bot, ball_x,
               ball_y):
    bottom_scal = bot_avg/sz_bot
    top_scal = top_avg/sz_top
    scal = (bottom_scal+top_scal)/2

    yNew = ball_y*scal
    return yNew