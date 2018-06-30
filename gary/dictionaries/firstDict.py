#!/usr/bin/env python3

def packer(**kwargs):
	print(kwargs)


def unpacker(name=None, greeting=None):
	if name and greeting:
		print("Hello, {} {}!".format(greeting, name))
	else:
		print("Hello, stranger!")



packer(name="Gary", greeting="Mr.")
unpacker(**{"name": "Gary", "greeting": "Mr."})