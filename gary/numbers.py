import random
import time

def game():
	secret_num = random.randint(1, 10)
	guesses = []

	while len(guesses) < 5:
		try:
			guessText = input("Guess a number between 1 & 10: ")
			guess = int(guessText)
		except ValueError:
			print("{} isn't a number you dummy!".format(guessText))
		else:
			if guess == secret_num:
				print("You got it! My number was {}!".format(secret_num))
				break
			elif guess > secret_num:
				print("My number is lower than {}".format(guessText))
			else:
				print("My number is higher than {}".format(guessText))
			guesses.append(guess)
			print("You have {} guesses left".format(5-len(guesses)))
	else:
		print("You didn't get it... My number was {}.".format(secret_num))
	play_again = input("Do you want to play again? Y/n: ")
	if play_again.lower() != 'n':
		game()
	else:
		print("Bye!")
game()
