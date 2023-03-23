import random
import pitchpredictor
import numpy

def rollpitch(pitcher_id, previous_pitch, pitch_num, count_list, stand):
	ball_type = ""
	try:
        ball_type = random.choices(["FB", "NonFB"], weights = pitchpredictor.getFastBallWeights(pitcher_id, previous_pitch, pitch_num, count_list, stand).tolist()[0])
	except:
        returm "FB"
	if ball_type == "FB":
		return "FB"
	else:
		ball_type = random.choices(["CH","CB","SL"], weights= pitchpredictor.getNonFastBallWeights(pitcher_id, previous_pitch, pitch_num, count_list, stand).tolist()[0])
		return ball_type

def pitch_outcome(pitch_type, batter_id, weights):
	return random.choices(["K","B","FOUL","SINGLE","DOUBLE","TRIPLE","HR","HBP"],weights = weights[pitch_type].loc[batter_id].tolist())

def atBat(ball_count, strike_count, batter_id, pitcher_id, previous_pitch, stand, weights, pitch_num):
	"""
 	ball_count - the number of balls that it starts at
  	strike_count - the number of strikes incurred
   	batter_id - MLB batter IDs
	pitcher_id - MLB pitcher IDs
 	previous_pitch - the result of the previous pitch
  	stand - left/right hand
   	weights - dictionary of weights for each batter for each type of ball hit
	pitch_num - the pitch # during the game
 	"""
	
	f = 0
	k = strike_count
	b = ball_count
	pitch_type = ""

	while True:
		pitch_thrown = rollpitch(pitcher_id, previous_pitch,pitch_num, [b,k], stand)[0]
		pitch = pitch_outcome(pitch_thrown, batter_id, weights)[0]
		
		
		
		if pitch == "FOUL":
			if k < 2:
				f += 1
				k += 1
			else:
				f += 1
		elif pitch == "K":
			k += 1
			if k >= 3:
				return "Strikeout", f+k+b, pitch_thrown
		elif pitch == "B":
			b += 1
			if b >= 4:
				return "Walk", f+k+b, pitch_thrown
		elif pitch == "SINGLE":
			return "Single", f+k+b+1, pitch_thrown
		elif pitch == "DOUBLE":
			return "Double", f+k+b+1, pitch_thrown
		elif pitch == "TRIPLE":
			return "Triple",f+k+b+1, pitch_thrown
		elif pitch == "HBP":
			return "HBP",f+k+b+1, pitch_thrown
		elif pitch == "HR":
			return "HR",f+k+b+1, pitch_thrown



##############################################





	
	# weight = 0
    # pitch 1, which only uses the weights corresponding to a 0-0 count

	# %fastball vs. %non-fastball
						# /|\
					# CB, ...
	#weight format: strikes, balls, fouls, singles, doubles, triples, home_runs, hbp
	# pitch_type = rollpitch(pitcher_id, previous_pitch,pitch_num, count_list, stand)
	# pitch1 = pitch_outcome(pitch_type, batter_id, weights)
	# # pitch_outcome(INSERT_WEIGHTS_HERE])[0]
	# if pitch1 == "FOUL":
	# 	f += 1
	# 	k += 1
	# elif pitch1 == "K":
	# 	k += 1
	# elif pitch1 == "B":
	# 	b += 1
	# elif pitch1 == "SINGLE":
	# 	return "SINGLE"
	# elif pitch1 == "DOUBLE":
	# 	return "DOUBLE"
	# elif pitch1 == "TRIPLE":
	# 	return "TRIPLE"
	# elif pitch1 == "HBP":
	# 	return "HBP"

  #   # pitch 2
  #   if k == 1: # testing for a 0-1 count
  #       # pitch2 = pitch_outcome(weights["0b1s"])[0]
		# pitch_type = rollpitch(pitcher_id, previous_pitch,pitch_num, count_list, stand)
		# pitch1 = pitch_outcome(pitch_type, batter_id, weights)
  #   elif b == 1: # testing for a 1-0 count
  #       # pitch2 = pitch_outcome(weights["1b0s"])[0]
		# pitch_type = rollpitch(pitcher_id, previous_pitch,pitch_num, count_list, stand)
		# pitch1 = pitch_outcome(pitch_type, batter_id, weights)
  #   if pitch2 == "FNS":
  #       f += 1
  #       k += 1
  #   elif pitch2 == "K":
  #       k += 1
  #   elif pitch2 == "B":
  #       b += 1
  #   elif pitch2 == "SINGLE":
  #       return "SINGLE"
  #   elif pitch2 == "DOUBLE":
  #       return "DOUBLE"
  #   else :
  #       return "HBP"
  
  #   # pitch 3
  #   if b == 2 and k == 0:
  #       pitch3 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 1 and k == 1:
  #       pitch3 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 0 and k == 2:
  #       pitch3 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
        
  #   if pitch3 == "FNS":
  #       if k < 2:
  #           k = k + 1
  #           f = f + 1
  #       else:
  #           f = f + 1
  #   elif pitch3 == "K":
  #       if k == 2:
  #           return "Strikeout"
  #       else:
  #           k = k + 1
  #   elif pitch3 == "B":
  #       b = b + 1
  #   elif pitch3 == "BIP":
  #       return "BIP"
  #   elif pitch3 == "BIPO":
  #       return "BIPO"
  #   else :
  #       return "HBP"
  
  #   # pitch 4
  #   if b == 1 and k == 2:
  #       pitch4 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 0 and k == 2:
  #       pitch4 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 2 and k == 1:
  #       pitch4 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 3 and k == 0:
  #       pitch4 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]

  #   if pitch4 == "FNS":
  #       if k < 2:
  #           k += 1 
  #       else:
  #           f = f + 1
  #   elif pitch4 == "K":
  #       if k == 2:
  #           return "Strikeout"
  #       else:
  #           k = k + 1
  #   elif pitch4 == "B":
  #       if b == 3:
  #           return "Walk"
  #       else:
  #           b = b + 1
  #   elif pitch4 == "BIP":
  #       return "BIP"
  #   elif pitch4 == "BIPO":
  #       return "BIPO"
  #   else:
  #       return "HBP"
    
  #   # pitch 5
  #   if b == 1 and k == 2:
  #       pitch5 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 0 and k == 2:
  #       pitch5 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 2 and k == 2:
  #       pitch5 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #   elif b == 3 and k == 1:
  #       pitch5 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]

  #   if pitch5 == "FNS":
  #       if k < 2:
  #           k = k + 1
  #           f = f + 1
  #       else:
  #           f = f + 1
  #   elif pitch5 == "K":
  #       if k == 2:
  #           return "Strikeout"
  #       else:
  #           k = k + 1
  #   elif pitch5 == "B":
  #       if b == 3:
  #           return "Walk"
  #       else:
  #           b = b + 1
  #   elif pitch5 == "BIP":
  #       return "BIP"
  #   elif pitch5 == "BIPO":
  #       return "BIPO"
  #   else:
  #       return "HBP"

  # # pitch 6, which is the last unique pitch and iterates until some outcome other than a foul ball occurs
  #   while True:
  #       if b == 1 and k == 2:
  #           pitch6 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #       elif b == 0 and k == 2:
  #           pitch6 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #       elif b == 2 and k == 2:
  #           pitch6 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
  #       elif b == 3 and k == 2:
  #           pitch6 = pitch_outcome(INSERT_WEIGHTS_HERE)[0]
            
  #       if pitch6 == "FNS":
  #           f = f + 1
  #       elif pitch6 == "K":
  #           return "Strikeout"
  #       elif pitch6 == "B":
  #           if b == 3:
  #               return "Walk"
  #           else:
  #               b = b + 1
  #       elif pitch6 == "BIP":
  #           return "BIP"
  #       elif pitch6 == "BIPO":
  #           return "BIPO"
  #       else:
  #           return "HBP"