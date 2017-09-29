# The function disemvowel takes a single word as a parameter and then returns that word at the end.
# I need you to make it so, inside of the function, all of the vowels ("a", "e", "i", "o", and "u") 
# are removed from the word. Solve this however you want, it's totally up to you!
# Oh, be sure to look for both uppercase and lower vowels!

word = ['a','b','c','d','E','f','g','h','i','j','k','l','m','n','O','p','q','r','s','t','u','v','w','y','z']
def disemvowel(word):

	for i in word:
		i = i.lower()
		try:
			word.remove('a')
		except ValueError:
			pass
		try:
			word.remove('e')
		except ValueError:
			pass		
		try:
			word.remove('i')
		except ValueError:
			pass
		try:
			word.remove('o')
		except ValueError:
			pass
		try:
			word.remove('u')
		except ValueError:
			break

	print (word)
	return word

disemvowel(word)