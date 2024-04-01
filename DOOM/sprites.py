from collections import deque
from math import sqrt, cos, atan2, degrees, inf
from typing import FrozenSet

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
				scale=(0.4, 0.4),
				side=30,
				animation=deque([
					pygame.image.load(f'../assets/sprites/barrel/animations/{i}.png').convert_alpha() for i in range(12)
				]),
				animation_dist=800,
				animation_speed=10,
				death_animation=deque([
					pygame.image.load(f'../assets/sprites/barrel/death/{i}.png').convert_alpha() for i in range(4)
				]),
				death_type=DeathType.NONE,
				death_shift=2.6,
				is_blocked=True,
				flag=Flag.DECORATION,
				object_action=deque()
			),
			SpriteType.PIN: SpriteParameters(
				sprite=pygame.image.load('../assets/sprites/pin/base/0.png').convert_alpha(),
				viewing_angles=False,
				shift=0.6,
				scale=(0.6, 0.6),
				side=30,
				animation=deque([
					pygame.image.load(f'../assets/sprites/pin/animations/{i}.png').convert_alpha() for i in range(8)
				]),
				animation_dist=800,
				animation_speed=10,
				death_type=DeathType.IMMORTAL,
				death_animation=deque(),
				death_shift=None,
				is_blocked=True,
				flag=Flag.DECORATION,
				object_action=deque()
			),
			SpriteType.DEVIL: SpriteParameters(
				sprite=[pygame.image.load(f'../assets/sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
				viewing_angles=True,
				shift=-0.2,
				scale=(1.1, 1.1),
				side=50,
				animation=deque(),
				animation_dist=150,
				animation_speed=10,
				death_animation=deque([
					pygame.image.load(f'../assets/sprites/devil/death/{i}.png').convert_alpha() for i in range(6)
				]),
				death_type=DeathType.NONE,
				death_shift=0.6,
				is_blocked=True,
				flag=Flag.NPC,
				object_action=deque([
					pygame.image.load(f'../assets/sprites/devil/animations/{i}.png').convert_alpha() for i in range(9)
				])
			),
			SpriteType.FLAME: SpriteParameters(
				sprite=pygame.image.load('../assets/sprites/flame/base/0.png').convert_alpha(),
				viewing_angles=False,
				shift=0.7,
				scale=(0.6, 0.6),
				side=30,
				animation=deque([
					pygame.image.load(f'../assets/sprites/flame/animations/{i}.png').convert_alpha()
					for i in range(15, 0, -1)
				]),
				animation_dist=800,
				animation_speed=5,
				death_animation=deque(),
				death_type=DeathType.IMMORTAL,
				death_shift=1.8,
				is_blocked=False,
				flag=Flag.DECORATION,
				object_action=deque()
			)
		}
		self.list_of_objects = [
			Sprite(self.sprite_parameters[SpriteType.BARREL], (7.1, 2.1)),
			Sprite(self.sprite_parameters[SpriteType.BARREL], (5.9, 2.1)),
			Sprite(self.sprite_parameters[SpriteType.PIN], (8.7, 2.5)),
			Sprite(self.sprite_parameters[SpriteType.DEVIL], (7, 4)),
			Sprite(self.sprite_parameters[SpriteType.FLAME], (8.6, 5.6))
		]

	@property
	def sprite_shot(self):
		return min([_object.is_on_fire for _object in self.list_of_objects], default=(inf, 0))


class Sprite:
	def __init__(self, parameters: SpriteParameters, position: Position) -> None:
		self.object = parameters.sprite.copy()
		self.viewing_angles = parameters.viewing_angles
		self.shift = parameters.shift
		self.scale = parameters.scale
		self.side = parameters.side
		self.x, self.y = position[0] * TILE, position[1] * TILE

		# Animation
		self.animation = parameters.animation.copy()
		self.animation_dist = parameters.animation_dist
		self.animation_speed = parameters.animation_speed
		self.animation_count = 0

		# Death
		self.death_animation = parameters.death_animation.copy()
		self.is_dead = parameters.is_dead
		self.death_type = parameters.death_type
		self.death_shift = parameters.death_shift
		self.dead_animation_count = 0

		# Other
		self.is_blocked = parameters.is_blocked
		self.flag = parameters.flag
		self.object_action = parameters.object_action.copy()

		self.npc_action_trigger = False
		self.door_open_trigger = False
		self.door_previous_position = self.y if self.flag == Flag.DOOR_H else self.x
		self.is_deleted = False

		if self.viewing_angles:
			if len(self.object) == 8:
				self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
				                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
			else:
				self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
				                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]

			self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

		# Defaults
		self.distance_to_sprite = 0.0
		self.theta = 0.0
		self.current_ray = 0
		self.projection_height = 0
		self.dead_sprite = None

	@property
	def position(self) -> Position:
		return self.x - self.side // 2, self.y - self.side // 2

	@property
	def is_on_fire(self) -> Tuple[float, int]:
		if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.is_blocked:
			return self.distance_to_sprite, self.projection_height

		return inf, 0

	def object_locate(self, player: Player) -> Tuple[float, Surface, Position] | Tuple[bool]:
		dx, dy = self.x - player.x, self.y - player.y
		self.distance_to_sprite: float = sqrt(dx ** 2 + dy ** 2)
		self.theta: float = atan2(dy, dx)
		gamma: float = self.theta - player.angle

		if dx > 0 and 180 <= degrees(player.angle) <= 360 or dx < 0 and dy < 0:
			gamma += DOUBLE_PI

		self.theta -= 1.4 * gamma

		self.current_ray: int = CENTER_RAY + int(gamma / DELTA_ANGLE)
		self.distance_to_sprite *= cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

		if 0 <= self.current_ray + FAKE_RAYS <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
			self.projection_height: int = min(int(PROJECTION_COEFFICIENT / self.distance_to_sprite), DOUBLE_HEIGHT)

			sprite_width: int = int(self.projection_height * self.scale[0])
			sprite_height: int = int(self.projection_height * self.scale[1])
			half_sprite_width: int = sprite_width // 2
			half_sprite_height: int = sprite_height // 2

			shift: float = half_sprite_height * self.shift

			if self.is_dead and self.death_type != DeathType.IMMORTAL:
				sprite_object: Surface = self.dead_animation()
				shift = half_sprite_height * self.death_shift
				sprite_height = int(sprite_height / 1.3)
			elif self.npc_action_trigger:
				sprite_object: Surface = self.npc_in_action()
			else:
				self.object = self.visible_sprite()
				sprite_object: Surface = self.sprite_animation()

			sprite_position: Position = self.current_ray * SCALE - half_sprite_height, HALF_HEIGHT - half_sprite_height + shift
			sprite: Surface = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))

			return self.distance_to_sprite, sprite, sprite_position
		else:
			return False,

	def sprite_animation(self) -> Surface | Surfaces:
		if self.animation and self.distance_to_sprite < self.animation_dist:
			sprite_object = self.animation[0]

			if self.animation_count < self.animation_speed:
				self.animation_count += 1
			else:
				self.animation.rotate()
				self.animation_count = 0

			return sprite_object

		return self.object

	def visible_sprite(self) -> FrozenSet[int] | Surface:
		if self.viewing_angles:
			if self.theta < 0:
				self.theta += DOUBLE_PI

			theta = 360 - int(degrees(self.theta))

			for angles in self.sprite_angles:
				if theta in angles:
					return self.sprite_positions[angles]

		return self.object

	def dead_animation(self) -> Surface:
		if len(self.death_animation):
			if self.dead_animation_count < self.animation_speed:
				self.dead_sprite = self.death_animation[0]
				self.dead_animation_count += 1
			else:
				self.dead_sprite = self.death_animation.popleft()
				self.dead_animation_count = 0

		return self.dead_sprite

	def npc_in_action(self) -> Surface:
		sprite_object: Surface = self.object_action[0]

		if self.animation_count < self.animation_speed:
			self.animation_count += 1
		else:
			self.object_action.rotate()
			self.animation_count = 0

		return sprite_object
