#!/usr/bin/env python3

lines = []             # Declare an empty list named "lines"
	with open ('lorem.txt', 'rt') as in_file:  # Open file lorem.txt for reading of text data.
		for line in in_file:   # For each line of text in in_file, where the data is named "line",
			lines.append(line)     # add that line to our list of lines.
			for element in lines:  # For each element in our list,
				print(element, end='')         # print it.