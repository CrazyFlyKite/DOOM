from math import sqrt, cos, atan2, degrees
from typing import Any

import pygame

from player import Player
from utilities import *


class Sprites:
	def __init__(self) -> None:
		self.sprite_types = {
			SpriteType.BARREL: pygame.image.load('../assets/sprites/barrel/0.png').convert_alpha(),
			SpriteType.PEDESTAL: pygame.image.load('../assets/sprites/pedestal/0.png').convert_alpha(),
			SpriteType.DEVIL: [pygame.image.load(f'../assets/sprites/devil/{i}.png').convert_alpha() for i in range(8)]
		}
		self.list_of_objects = {
			Sprite(self.sprite_types[SpriteType.BARREL], True, (7.1, 2.1), 1.8, 0.4),
			Sprite(self.sprite_types[SpriteType.BARREL], True, (5.9, 2.1), 1.8, 0.4),
			Sprite(self.sprite_types[SpriteType.PEDESTAL], True, (8.8, 2.5), 1.6, 0.5),
			Sprite(self.sprite_types[SpriteType.PEDESTAL], True, (8.8, 5.6), 1.6, 0.5),
			Sprite(self.sprite_types[SpriteType.DEVIL], False, (7, 4), -0.2, 0.7)
		}


class Sprite:
	def __init__(self, _object: Surface | List[Surface], is_static: bool, position: Position, shift: float,
	             scale: float) -> None:
		self._object = _object
		self._is_static = is_static
		self._x, self._y = position[0] * TILE, position[1] * TILE
		self._shift = shift
		self._scale = scale

		if not is_static:
			self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
			self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self._object)}

	@property
	def object(self) -> Surface | List[Surface]:
		return self._object

	@object.setter
	def object(self, value: Any) -> None:
		self._object = value

	@property
	def is_static(self) -> bool:
		return self._is_static

	@property
	def x(self) -> Number:
		return self._x

	@property
	def y(self) -> Number:
		return self._y

	@property
	def shift(self) -> float:
		return self._shift

	@property
	def scale(self) -> float:
		return self._scale

	def object_locate(self, player: Player, walls: Walls) -> Tuple[float, Surface, Position] | Tuple[bool]:
		fake_walls: Walls = [walls[0] for _ in range(FAKE_RAYS)] + walls + [walls[-1] for _ in range(FAKE_RAYS)]
		dx, dy = self.x - player.x, self.y - player.y
		distance_to_sprite: float = sqrt(dx ** 2 + dy ** 2)
		theta: float = atan2(dy, dx)
		gamma: float = theta - player.angle

		if dx > 0 and 180 <= degrees(player.angle) <= 360 or dx < 0 and dy < 0:
			gamma += DOUBLE_PI

		delta_rays: int = int(gamma / DELTA_ANGLE)
		current_ray: int = CENTER_RAY + delta_rays
		distance_to_sprite *= cos(HALF_FOV - current_ray * DELTA_ANGLE)

		fake_ray: int = current_ray + FAKE_RAYS
		if 0 <= fake_ray <= NUMBER_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
			projection_height: int = int(PROJECTION_COEFFICIENT / distance_to_sprite * self.scale)
			half_projection_height: int = projection_height // 2
			shift: float = half_projection_height * self.shift

			if not self.is_static:
				if theta < 0:
					theta += DOUBLE_PI

				theta = 360 - int(degrees(theta))

				for angles in self.sprite_angles:
					if theta in angles:
						self.object = self.sprite_positions[angles]
						break

					self.object = self.sprite_positions[angles]

			sprite_position: Position = current_ray * SCALE - half_projection_height, HALF_HEIGHT - half_projection_height + shift
			sprite: Surface = pygame.transform.scale(self.object, (projection_height, projection_height))

			return distance_to_sprite, sprite, sprite_position
		else:
			return False,
