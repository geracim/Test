# OK, I need you to finish writing a function for me. 
# The function disemvowel takes a single word as a parameter
# and then returns that word at the end.
# I need you to make it so, inside of the function, all
# of the vowels ("a", "e", "i", "o", and "u") are removed
# from the word. Solve this however you want, it's totally up to you!
# Oh, be sure to look for both uppercase and lowercase vowels!

word_list = ["A","b","c","d","e","F","g","h","I","j","k","l","m","n","o","p","q","r","s","t","U","v","w","x","y","z"]

def disemvowel(word_list):
	
	for item in word_list:
		if item.lower() == "a":
			try:
				word_list.remove(item)
			except ValueError:
				continue
		elif item.lower() == "e":
			try:
				word_list.remove(item)
			except ValueError:
				continue
		elif item.lower() == "i":
			try:
				word_list.remove(item)
			except ValueError:
				continue
		elif item.lower() == "o":
			try:
				word_list.remove(item)
			except ValueError:
				continue
		elif item.lower() == "u":
			try:
				word_list.remove(item)
			except ValueError:
				continue
	print(word_list)

disemvowel(word_list)