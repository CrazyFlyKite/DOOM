from math import sin, cos

import pygame

from map import world_map
from utilities import *


def mapping(a: float, b: float) -> Position:
	return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(screen: pygame.Surface, player_position: Position, player_angle: float) -> None:
	ox, oy = player_position
	xm, ym = mapping(ox, oy)
	current_angle: float = player_angle - HALF_FOV

	for ray in range(NUMBER_RAYS):
		sin_a, cos_a = sin(current_angle), cos(current_angle)

		# Verticals
		x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)

		for i in range(0, WIDTH, TILE):
			depth_v: float = (x - ox) / cos_a
			y: float = oy + depth_v * sin_a

			if mapping(x + dx, y) in world_map:
				break

			x += dx * TILE

		# Horizontals
		y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)

		for i in range(0, HEIGHT, TILE):
			depth_h: float = (y - oy) / sin_a
			x: float = ox + depth_h * cos_a

			if mapping(x, y + dy) in world_map:
				break

			y += dy * TILE

		# Projection
		depth: float = (depth_v if depth_v < depth_h else depth_h) * cos(player_angle - current_angle)  # NOQA
		depth = max(depth, 0.00001)
		projection_height: int = min(int(PROJECTION_COEFFICIENT / depth), 2 * HEIGHT)

		# Draw
		color: int = int(255 / (1 + depth * depth * 0.00002))
		pygame.draw.rect(screen, (color, color // 2, color // 2),
		                 (ray * SCALE, HALF_HEIGHT - projection_height // 2, SCALE, projection_height))

		current_angle += DELTA_ANGLE
