from math import sin, cos, floor

import pygame

from map import mini_map
from player import Player
from ray_casting import ray_casting
from utilities import *


class Drawing:
	def __init__(self, screen: pygame.Surface, screen_map: pygame.Surface) -> None:
		self.screen = screen
		self.screen_map = screen_map
		self.font = pygame.font.SysFont('Arial', 30, bold=True)

	def background(self) -> None:
		pygame.draw.rect(self.screen, SKY_BLUE, (0, 0, WIDTH, HALF_HEIGHT))
		pygame.draw.rect(self.screen, DARK_GRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

	def world(self, player_position: Position, player_angle: float) -> None:
		ray_casting(self.screen, player_position, player_angle)

	def fps(self, clock: pygame.time.Clock) -> None:
		self.screen.blit(self.font.render(str(floor(clock.get_fps())), 0, RED), FPS_POSITION)

	def mini_map(self, player: Player) -> None:
		self.screen_map.fill(BLACK)
		map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
		pygame.draw.line(self.screen_map, YELLOW, (map_x, map_y),
		                 (map_x + 12 * cos(player.angle), map_y + 12 * sin(player.angle)), 3)
		pygame.draw.circle(self.screen_map, RED, (map_x, map_y), 5)

		for x, y in mini_map:
			pygame.draw.rect(self.screen_map, GREEN, (x, y, MAP_TILE, MAP_TILE))

		self.screen.blit(self.screen_map, MAP_POSITION)
