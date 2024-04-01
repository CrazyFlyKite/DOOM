from contextlib import redirect_stdout
from warnings import filterwarnings

filterwarnings('ignore')

# Disable Pygame welcome message
with redirect_stdout(None):
	import pygame
	from pygame.time import Clock

from drawing import Drawing
from interaction import Interaction
from player import Player
from utilities import *
from sprites import Sprites
from ray_casting import ray_casting_walls

# Initialize Pygame
pygame.init()

# Initialize variables
screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
mini_map: Surface = Surface(MINIMAP_RESOLUTION)
pygame.mouse.set_visible(False)

sprites: Sprites = Sprites()
clock: Clock = Clock()
player: Player = Player(sprites)
drawing: Drawing = Drawing(screen, mini_map, player)
interaction: Interaction = Interaction(player, sprites, drawing)

if __name__ == '__main__':
	while True:
		# Move player_position
		player.move()

		# Draw
		drawing.background(player.angle)
		walls, wall_shot = ray_casting_walls(player, drawing.textures)
		drawing.world(walls + [sprite.object_locate(player) for sprite in sprites.list_of_objects])
		drawing.fps(clock)
		drawing.mini_map(player)
		drawing.player_weapon([wall_shot, sprites.sprite_shot])
		interaction.interaction_objects()

		# Other
		pygame.display.flip()
		clock.tick(FPS)
