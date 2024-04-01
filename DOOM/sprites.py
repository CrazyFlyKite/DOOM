from collections import deque
from math import sqrt, cos, atan2, degrees

import pygame

from player import Player
from utilities import *


class Sprites:
	def __init__(self) -> None:
		self.sprite_parameters = {
			SpriteType.BARREL: SpriteParameters(
				sprite=pygame.image.load('../assets/sprites/barrel/base/0.png').convert_alpha(),
				viewing_angles=False,
				shift=1.8,
				scale=0.4,
				animation=deque([
					pygame.image.load(f'../assets/sprites/barrel/animations/{i}.png').convert_alpha() for i in range(12)
				]),
				animation_dist=800,
				animation_speed=10,
				blocked=False
			),
			SpriteType.PIN: SpriteParameters(
				sprite=pygame.image.load('../assets/sprites/pin/base/0.png').convert_alpha(),
				viewing_angles=False,
				shift=0.6,
				scale=0.6,
				animation=deque([
					pygame.image.load(f'../assets/sprites/pin/animations/{i}.png').convert_alpha() for i in range(8)
				]),
				animation_dist=800,
				animation_speed=10,
				blocked=True,
			),
			SpriteType.DEVIL: SpriteParameters(
				sprite=[pygame.image.load(f'../assets/sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
				viewing_angles=True,
				shift=-0.2,
				scale=1.1,
				animation=deque([
					pygame.image.load(f'../assets/sprites/devil/animations/{i}.png').convert_alpha() for i in range(9)
				]),
				animation_dist=150,
				animation_speed=10,
				blocked=True,
			),
			SpriteType.FLAME: SpriteParameters(
				sprite=pygame.image.load('../assets/sprites/flame/base/0.png').convert_alpha(),
				viewing_angles=False,
				shift=0.7,
				scale=0.6,
				animation=deque([
					pygame.image.load(f'../assets/sprites/flame/animations/{i}.png').convert_alpha()
					for i in range(15, 0, -1)
				]),
				animation_dist=800,
				animation_speed=5,
				blocked=False,
			)
		}
		self.list_of_objects = [
			Sprite(self.sprite_parameters[SpriteType.BARREL], (7.1, 2.1)),
			Sprite(self.sprite_parameters[SpriteType.BARREL], (5.9, 2.1)),
			Sprite(self.sprite_parameters[SpriteType.PIN], (8.7, 2.5)),
			Sprite(self.sprite_parameters[SpriteType.DEVIL], (7, 4)),
			Sprite(self.sprite_parameters[SpriteType.FLAME], (8.6, 5.6))
		]


class Sprite:
	def __init__(self, parameters: SpriteParameters, position: Position) -> None:
		self.object = parameters.sprite
		self.viewing_angles = parameters.viewing_angles
		self.shift = parameters.shift
		self.scale = parameters.scale
		self.animation = parameters.animation
		self.animation_dist = parameters.animation_dist
		self.animation_speed = parameters.animation_speed
		self.animation_count = 0
		self.blocked = parameters.blocked
		self.side = 30
		self.x, self.y = position[0] * TILE, position[1] * TILE

		if self.viewing_angles:
			self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
			self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

	@property
	def position(self) -> Position:
		return self.x - self.side // 2, self.y - self.side // 2

	def object_locate(self, player: Player) -> Tuple[float, Surface, Position] | Tuple[bool]:
		dx, dy = self.x - player.x, self.y - player.y
		distance_to_sprite: float = sqrt(dx ** 2 + dy ** 2)
		theta: float = atan2(dy, dx)
		gamma: float = theta - player.angle

		if dx > 0 and 180 <= degrees(player.angle) <= 360 or dx < 0 and dy < 0:
			gamma += DOUBLE_PI

		current_ray: int = CENTER_RAY + int(gamma / DELTA_ANGLE)
		distance_to_sprite *= cos(HALF_FOV - current_ray * DELTA_ANGLE)

		if 0 <= current_ray + FAKE_RAYS <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
			projection_height: int = min(int(PROJECTION_COEFFICIENT / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
			half_projection_height: int = projection_height // 2
			shift: float = half_projection_height * self.shift

			# Selecting sprite for angle
			if self.viewing_angles:
				if theta < 0:
					theta += DOUBLE_PI

				theta = 360 - int(degrees(theta))

				for angles in self.sprite_angles:
					if theta in angles:
						self.object = self.sprite_positions[angles]
						break

					self.object = self.sprite_positions[angles]

			# Sprite animations
			sprite_object: Surface = self.object
			if self.animation and distance_to_sprite < self.animation_dist:
				sprite_object = self.animation[0]

				if self.animation_count < self.animation_speed:
					self.animation_count += 1
				else:
					self.animation.rotate()
					self.animation_count = 0

			sprite_position: Position = current_ray * SCALE - half_projection_height, HALF_HEIGHT - half_projection_height + shift
			sprite: Surface = pygame.transform.scale(sprite_object, (projection_height, projection_height))

			return distance_to_sprite, sprite, sprite_position
		else:
			return False,
