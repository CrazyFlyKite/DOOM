from math import sin, cos, degrees

import pygame

from map import mini_map
from player import Player
from utilities import *


class Drawing:
	def __init__(self, screen: Surface, screen_map: Surface) -> None:
		self.screen = screen
		self.screen_map = screen_map
		self.font = pygame.font.SysFont('Arial', 30, bold=True)
		self.textures = {
			ElementType.WALL1: pygame.image.load('../assets/images/wall 1.png').convert(),
			ElementType.WALL2: pygame.image.load('../assets/images/wall 2.png').convert(),
			ElementType.WALL3: pygame.image.load('../assets/images/wall 3.png').convert(),
			ElementType.WALL4: pygame.image.load('../assets/images/wall 4.png').convert(),
			ElementType.SKY: pygame.image.load('../assets/images/sky.png').convert()
		}

	def background(self, angle: float) -> None:
		sky_offset: float = -5 * degrees(angle) % WIDTH
		self.screen.blit(self.textures[ElementType.SKY], (sky_offset, 0))
		self.screen.blit(self.textures[ElementType.SKY], (sky_offset - WIDTH, 0))
		self.screen.blit(self.textures[ElementType.SKY], (sky_offset + WIDTH, 0))
		pygame.draw.rect(self.screen, DARK_GRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

	def world(self, world_objects: Walls) -> None:
		for obj in sorted(world_objects, key=lambda x: x[0], reverse=True):
			if obj[0]:
				_, object_, object_position = obj
				self.screen.blit(object_, object_position)

	def fps(self, clock: pygame.time.Clock) -> None:
		self.screen.blit(self.font.render(str(int(clock.get_fps())), 0, DARK_ORANGE), FPS_POSITION)

	def mini_map(self, player: Player) -> None:
		self.screen_map.fill(BLACK)
		map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
		pygame.draw.line(self.screen_map, YELLOW, (map_x, map_y),
		                 (map_x + 12 * cos(player.angle), map_y + 12 * sin(player.angle)), 3)
		pygame.draw.circle(self.screen_map, RED, (map_x, map_y), 5)

		for x, y in mini_map:
			pygame.draw.rect(self.screen_map, DARK_BROWN, (x, y, MAP_TILE, MAP_TILE))

		self.screen.blit(self.screen_map, MAP_POSITION)
