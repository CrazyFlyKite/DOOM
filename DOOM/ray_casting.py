from math import sin, cos

import pygame
from numba import njit
from numba.typed.typeddict import Dict as NumbaDict

from map import world_map, WORLD_WIDTH, WORLD_HEIGHT
from player import Player
from utilities import *


@njit(fastmath=True)
def mapping(a: float, b: float) -> Position:
	return (a // TILE) * TILE, (b // TILE) * TILE


@njit(fastmath=True)
def ray_casting(player_position: Position, player_angle: float, _world_map: NumbaDict) -> RayCastedWalls:
	casted_walls: RayCastedWalls = []
	ox, oy = player_position
	xm, ym = mapping(ox, oy)
	texture_v = texture_h = WALL1
	current_angle: float = player_angle - HALF_FOV

	for ray in range(NUMBER_RAYS):
		sin_a, cos_a = sin(current_angle), cos(current_angle)

		# Verticals
		x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)

		for i in range(0, WORLD_WIDTH, TILE):
			depth_v: float = (x - ox) / cos_a
			yv: float = oy + depth_v * sin_a
			tile_v: Position = mapping(x + dx, yv)

			if tile_v in _world_map:
				texture_v: int = _world_map[tile_v]
				break

			x += dx * TILE

		# Horizontals
		y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)

		for i in range(0, WORLD_HEIGHT, TILE):
			depth_h: float = (y - oy) / sin_a
			xh: float = ox + depth_h * cos_a
			tile_h: Position = mapping(xh, y + dy)

			if tile_h in _world_map:
				texture_h: int = _world_map[tile_h]
				break

			y += dy * TILE

		# Projection
		depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)  # NOQA
		offset = int(offset) % TILE
		depth *= cos(player_angle - current_angle)
		depth = max(depth, 0.00001)
		projection_height: int = min(int(PROJECTION_COEFFICIENT / depth), PENTA_HEIGHT)
		casted_walls.append((depth, offset, projection_height, texture))

		current_angle += DELTA_ANGLE

	return casted_walls


def ray_casting_walls(player: Player, textures: Surfaces) -> Walls:
	casted_walls: RayCastedWalls = ray_casting(player.position, player.angle, world_map)
	walls: Walls = []

	for ray, casted_values in enumerate(casted_walls):
		depth, offset, projection_height, texture = casted_values
		wall_column: Surface = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
		wall_column = pygame.transform.scale(wall_column, (SCALE, projection_height))
		wall_position: Position = (ray * SCALE, HALF_HEIGHT - projection_height // 2)
		walls.append((depth, wall_column, wall_position))

	return walls
