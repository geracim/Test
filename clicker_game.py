import random

# parsing txt file for variable values
# execfile(file_content)


p1_level = 1
p1_exp = 0
control = 0

while play == True:
# create floating score variable - later will add score to this variable each consecutive play until player chooses to Save which adds this value to the p1_exp value.
    floating_score = p1_exp   
# provide menu
    menu_choice = str(input("""
        Enter 'p' to play.
        Enter 's' to see score.
        Enter 'q' to save and quit.
        Enter 'n' to start new game.
        
        """))
# create conditions by which to show score, enter game, or quit.
    if menu_choice == "p":
        #########PLAY########
        if p1_exp > 0:
            play_game()
        control = 1
        continue
    elif menu_choice == "s":
        #########SHOW SCORE#########
        print ("Your current level: {}".format(p1_level))
        print ("Your current experience: {}".format(p1_exp))
        control = 2
        continue
    elif menu_choice == "q":
        #########QUIT GAME##########
        p1_exp = floating_score
        print ("See you next time!")
        break
    elif menu_choice == "n":
        #########Wipe Progress##########
        p1_exp = 0
        p1_level = 1
        print ("Your progress has been wiped.")
        
        continue

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
