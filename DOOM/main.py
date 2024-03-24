import sys

import pygame

from drawing import Drawing
from player import Player
from utilities import *

# Initialize Pygame
pygame.init()

# Initialize variables
screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
screen_map: pygame.Surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
clock: pygame.time.Clock = pygame.time.Clock()
player: Player = Player()
drawing: Drawing = Drawing(screen, screen_map)

if __name__ == '__main__':
	while True:
		# Check for exit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

		# Move player
		player.move()

		# Draw
		drawing.background(player.angle)
		drawing.world(player.position, player.angle)
		drawing.fps(clock)
		drawing.mini_map(player)

		# Other
		pygame.display.flip()
		clock.tick(FPS)
