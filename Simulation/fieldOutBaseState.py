import random
import pickle

with open('/Users/moksh/Desktop/OutOrNot/stands_dict.pickle','rb') as f:
    stands = pickle.load(f)
    
    
    
def fieldOutBaseState(base_state, batter_id):
    if stands[batter_id] == 'R':
        weights = [.4, .35, .25]
    elif stands[batter_id] == 'L':
        weights = [.25, .35, .4]

    if base_state != 0:
        if base_state == 1:
            return random.choices([1, 1, 0], weights=weights, k=1)
        elif base_state == 10:
            return random.choices([10, 0, 10], weights=weights, k=1)
        elif base_state == 100:
            return random.choices([0, 100, 100], weights=weights, k=1)
        elif base_state == 11:
            return random.choices([11, 1, 10], weights=weights, k=1)
        elif base_state == 110:
            return random.choices([10, 100, 110], weights=weights, k=1)
        elif base_state == 101:
            return random.choices([1, 101, 100], weights=weights, k=1)
        elif base_state == 111:
            return random.choices([11, 101, 110], weights=weights, k=1)
    else:
        return [base_state]