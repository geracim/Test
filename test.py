arg = "3"
def squared(arg):
	try:
		arg = int(arg)
		return (arg * arg)
	except ValueError:
		return arg * len(arg)

squared(arg)

# squared(5) would return 25
# squared("2") would return 4
# squared("tim") would return "timtimtim"