#!/usr/bin/env python3

def lesson1():
	messy_list = [4,2,1,3,5]
	print("original: {}".format(messy_list))
	messy_list.sort()
	print("modified-sorted: {}".format(messy_list))

	messy_list = [4,2,1,3,5]
	print("original again: {}".format(messy_list))

	clean_list = messy_list[:]
	clean_list.sort()

	print("sorted-copy: {}".format(clean_list))

############# Stepping through Slices ################

def lesson2():
	num_list = list(range(20))
	print("Original numbers list: {}".format(num_list))

	print(num_list[::-1])


lesson2()