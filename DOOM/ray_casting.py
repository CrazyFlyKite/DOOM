from math import sin, cos
from typing import Dict

import pygame

from map import world_map
from utilities import *


def mapping(a: float, b: float) -> Position:
	return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(screen: pygame.Surface, player_position: Position, player_angle: float,
                textures: Dict[str, pygame.Surface]) -> None:
	ox, oy = player_position
	xm, ym = mapping(ox, oy)
	current_angle: float = player_angle - HALF_FOV

	for ray in range(NUMBER_RAYS):
		sin_a, cos_a = sin(current_angle), cos(current_angle)

		# Verticals
		x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)

		for i in range(0, WIDTH, TILE):
			depth_v: float = (x - ox) / cos_a
			yv: float = oy + depth_v * sin_a
			tile_v: Position = mapping(x + dx, yv)

			if tile_v in world_map:
				texture_v: str = world_map[tile_v]
				break

			x += dx * TILE

		# Horizontals
		y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)

		for i in range(0, HEIGHT, TILE):
			depth_h: float = (y - oy) / sin_a
			xh: float = ox + depth_h * cos_a
			tile_h: Position = mapping(xh, y + dy)

			if tile_h in world_map:
				texture_h: str = world_map[tile_h]
				break

			y += dy * TILE

		# Projection
		depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)  # NOQA
		offset = int(offset) % TILE
		depth *= cos(player_angle - current_angle)
		depth = max(depth, 0.00001)
		projection_height: int = min(int(PROJECTION_COEFFICIENT / depth), 2 * HEIGHT)

		# Draw textures
		wall_column: pygame.Surface = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE,
		                                                           TEXTURE_HEIGHT)
		wall_column = pygame.transform.scale(wall_column, (SCALE, projection_height))
		screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - projection_height // 2))

		current_angle += DELTA_ANGLE
