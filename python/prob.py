def calculate_probability(prob_of_reaching, prob_of_next):
    return prob_of_reaching * prob_of_next

def calculate_win_probability(inning, outs, home_score, away_score, bases):
    return calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, 1, 1)

""" BASES """
""" 1 : 000 """
""" 2 : 001 """
""" 3 : 010 """
""" 4 : 011 """
""" 5 : 100 """
""" 6 : 101 """
""" 7 : 110 """
""" 8 : 111 """
def calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, current_probability, next_action_probability):
    if current_probability < 1e-4:
        return current_probability * int(home_score > away_score)   
    cumulative_win_probability = 0.0
    # SINGLE

    # DOUBLE

    # TRIPLE

    # HOME RUN

    # STRIKEOUT
    strikeout_probability = ...
    if outs == 2:
        inning += 1
        outs = 0
        bases = [0, 0, 0]
    else:
        outs += 1
    cumulative_win_probability += calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, current_probability, strikeout_probability)

    # FLYOUT
    if bases[0] == 1:
        bases[0] = 0
        if inning % 2 == 0:
            home_score += 1
        else: 
            away_score += 1
    
    if bases[1] == 1:
        bases[0] = 1
    
    if outs == 2:
        inning += 1
        outs = 0
        bases = [0, 0, 0]
    
    cumulative_win_probability += calculate_win_probability_wrapper(inning, outs, bases, home_score, away_score, current_probability, strikeout_probability)

    # GB OUT