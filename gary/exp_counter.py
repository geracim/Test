import pygame, time
from pygame.locals import *

p1_level = 1
p1_exp = 0
lvl1_exp = 100
lvl2_exp = 300
lvl3_exp = 500

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Keyboard Test')
pygame.mouse.set_visible(0)


while True:
	for event in pygame.event.get():
		if (event.type == KEYUP) or (event.type == KEYDOWN):
			p1_exp = p1_exp + 20
			print("You gained 20exp! Your total is: {}".format(p1_exp))
			time.sleep(0.1)