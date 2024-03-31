import sys
from contextlib import redirect_stdout

with redirect_stdout(None):
	import pygame

from drawing import Drawing
from player import Player
from utilities import *
from sprites import Sprites
from ray_casting import ray_casting

# Initialize Pygame
pygame.init()

# Initialize variables
screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
mini_map: Surface = Surface(MINIMAP_RESOLUTION)
pygame.mouse.set_visible(False)
clock: pygame.time.Clock = pygame.time.Clock()
player: Player = Player()
sprites: Sprites = Sprites()
drawing: Drawing = Drawing(screen, mini_map)

if __name__ == '__main__':
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

		# Move player
		player.move()

		# Draw
		drawing.background(player.angle)
		walls: Walls = ray_casting(player, drawing.textures)
		drawing.world(walls + [_object.object_locate(player) for _object in sprites.list_of_objects])
		drawing.fps(clock)
		drawing.mini_map(player)

		# Other
		pygame.display.flip()
		clock.tick(FPS)
