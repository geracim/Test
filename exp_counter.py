p1_level = 1
p1_exp = 0
lvl1_exp = 100
lvl2_exp = 300
lvl3_exp = 500




user_input = input("tap space key to gain experience")
while True:
	if user_input == " ":
		p1_exp = p1_exp + 20
		print("You gained 20exp! Your total is: {}".format(p1_exp))
	else:
		print("You didn't follow directions")