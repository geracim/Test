import random

# parsing txt file for variable values
# execfile(file_content)


p1_level = 1
p1_exp = 0
play = True

while play == True:
# create floating score variable - later will add score to this variable each consecutive play until player chooses to Save which adds this value to the p1_exp value.
    floating_score = p1_exp   
# provide menu
    menu_choice = str(input("""
        Enter 'Play' to continue.
        Enter 'Score' to see score.
        Enter 'Quit' to save and quit.
        Enter 'New' to start new game.
        
        """))
# create conditions by which to show score, enter game, or quit.
    if menu_choice = str("Play"):
        #########PLAY########
        continue
    else if menu_choice = str("Score"):
        #########SHOW SCORE#########
        continue
    else if menu_choice = str("Quit"):
        #########QUIT GAME##########
        p1_exp = floating_score
        break
    else 
# base_gen randomly generates the base value for exp calculation. simulates a d20 throw
    base_gen = random.randint(1, 20)
# multiplier is the p1_level + half the difference between the player's current experience & the base_gen
    multiplier = abs(int(p1_level + (0.5) * (p1_exp - base_gen)))
    print("You earned {} points!".format(multiplier))
# ask user if they want to see current score
    user_input = int(input("Enter 1 to save current score. Enter 2 keep playing (unsaved). "))
    if user_input == 1:
        print("Your total points: {}".format(multiplier+p1_exp))
    elif user_input == 2:
        continue
    else:
        print("Goodbye!")
        break
