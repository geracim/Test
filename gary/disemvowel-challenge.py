word = ["a","b","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def disemvowel(word):
	vowels = ["a", "e", "i", "o", "u"]
	for x in word.lower():
		if x in vowels:
			try:
				word.remove(x)
			except ValueError:
				pass

	return word

disemvowel(word)