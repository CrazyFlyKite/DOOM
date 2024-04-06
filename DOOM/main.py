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

sprites: Sprites = Sprites()
clock: Clock = Clock()
player: Player = Player(sprites)
drawing: Drawing = Drawing(screen, mini_map, player, clock)
interaction: Interaction = Interaction(player, sprites, drawing)

interaction.play_music()
drawing.menu()

if __name__ == '__main__':
	while True:
		# Move
		player.move()

		# Draw
		drawing.background(player.angle)
		walls, wall_shot = ray_casting_walls(player, drawing.textures)
		drawing.world(walls + [sprite.object_locate(player) for sprite in sprites.list_of_objects])
		drawing.fps()
		drawing.mini_map(player)
		drawing.player_weapon([wall_shot, sprites.sprite_shot])

		# Interaction
		interaction.interaction_objects()
		interaction.npc_action()
		interaction.check_win()

		# Other
		pygame.display.flip()
		clock.tick(FPS)
