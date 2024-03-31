import sys
from math import sin, cos
from typing import Any

import pygame

from map import collision_walls
from utilities import *


class Player:
	def __init__(self, sprites: 'Sprites') -> None:  # NOQA
		self._x, self._y = PLAYER_POSITION
		self._angle = PLAYER_ANGLE
		self._rect = pygame.Rect(*PLAYER_POSITION, PLAYER_SIDE, PLAYER_SIDE)
		self._collision_list = collision_walls + [pygame.Rect(*sprite.position, sprite.side, sprite.side)
		                                          for sprite in sprites.list_of_objects if sprite.is_blocked]

	@property
	def x(self) -> Number:
		return self._x

	@x.setter
	def x(self, value: Any) -> None:
		self._x = float(value)

	@property
	def y(self) -> Number:
		return self._y

	@y.setter
	def y(self, value: Any) -> None:
		self._y = float(value)

	@property
	def position(self) -> Position:
		return int(self.x), int(self.y)

	@property
	def angle(self) -> float:
		return self._angle

	@angle.setter
	def angle(self, value: Any) -> None:
		self._angle = float(value)

	@property
	def rect(self) -> pygame.Rect:
		return self._rect

	@property
	def collision_list(self) -> List[pygame.Rect]:
		return self._collision_list

	def detect_collision(self, dx: float, dy: float) -> None:
		next_rect: pygame.Rect = self.rect.copy()
		next_rect.move_ip(dx, dy)

		if len(hit_indices := next_rect.collidelistall(self.collision_list)):
			delta_x = delta_y = 0

			for hit_index in hit_indices:
				hit_rect = self.collision_list[hit_index]

				if dx > 0:
					delta_x += next_rect.right - hit_rect.left
				else:
					delta_x += hit_rect.right - next_rect.left

				if dy > 0:
					delta_y += next_rect.bottom - hit_rect.top
				else:
					delta_y += hit_rect.bottom - next_rect.top

			if abs(delta_x - delta_y) < 10:
				dx = dy = 0
			elif delta_x > delta_y:
				dy = 0
			elif delta_x < delta_y:
				dx = 0

		self.x += dx
		self.y += dy

	def move(self) -> None:
		self.key_control()
		self.rect.center = self.position
		self.mouse_control()
		self.angle %= DOUBLE_PI

	def key_control(self) -> None:
		sin_a, cos_a = sin(self.angle), cos(self.angle)
		keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

		# Exit
		if keys[pygame.K_ESCAPE]:
			sys.exit(0)

		# Move
		if keys[pygame.K_w]:
			dx = PLAYER_SPEED * cos_a
			dy = PLAYER_SPEED * sin_a
			self.detect_collision(dx, dy)

		if keys[pygame.K_s]:
			dx = -PLAYER_SPEED * cos_a
			dy = -PLAYER_SPEED * sin_a
			self.detect_collision(dx, dy)

		if keys[pygame.K_a]:
			dx = PLAYER_SPEED * sin_a
			dy = -PLAYER_SPEED * cos_a
			self.detect_collision(dx, dy)

		if keys[pygame.K_d]:
			dx = -PLAYER_SPEED * sin_a
			dy = PLAYER_SPEED * cos_a
			self.detect_collision(dx, dy)

		# Rotate
		if keys[pygame.K_LEFT]:
			self.angle -= PLAYER_ROTATION_SPEED

		if keys[pygame.K_RIGHT]:
			self.angle += PLAYER_ROTATION_SPEED

	def mouse_control(self) -> None:
		if pygame.mouse.get_focused():
			difference: int = pygame.mouse.get_pos()[0] - HALF_WIDTH
			pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
			self.angle += difference * PLAYER_MOUSE_SENSITIVITY
