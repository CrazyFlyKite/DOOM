from math import sin, cos
from typing import Any

import pygame

from utilities import *


class Player:
	def __init__(self) -> None:
		self._x, self._y = PLAYER_POSITION
		self._angle = PLAYER_ANGLE

	@property
	def x(self) -> float:
		return self._x

	@x.setter
	def x(self, value: Any) -> None:
		self._x = float(value)

	@property
	def y(self) -> float:
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

	def move(self) -> None:
		sin_a, cos_a = sin(self.angle), cos(self.angle)
		keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

		# Move
		if keys[pygame.K_w]:
			self.x += PLAYER_SPEED * cos_a
			self.y += PLAYER_SPEED * sin_a

		if keys[pygame.K_s]:
			self.x += -PLAYER_SPEED * cos_a
			self.y += -PLAYER_SPEED * sin_a

		if keys[pygame.K_a]:
			self.x += PLAYER_SPEED * sin_a
			self.y += -PLAYER_SPEED * cos_a

		if keys[pygame.K_d]:
			self.x += -PLAYER_SPEED * sin_a
			self.y += PLAYER_SPEED * cos_a

		# Rotate
		if keys[pygame.K_LEFT]:
			self.angle -= 0.02

		if keys[pygame.K_RIGHT]:
			self.angle += 0.02
