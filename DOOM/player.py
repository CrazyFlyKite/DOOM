from math import sin, cos

import pygame

from map import collision_walls
from utilities import *


class Player:
	def __init__(self, sprites: 'Sprites') -> None:  # NOQA
		self.x, self.y = PLAYER_POSITION
		self.angle = PLAYER_ANGLE
		self.rect = pygame.Rect(*PLAYER_POSITION, PLAYER_SIDE, PLAYER_SIDE)
		self.sprites = sprites
		self.shot = False

	@property
	def position(self) -> Position:
		return int(self.x), int(self.y)

	@property
	def collision_list(self) -> List[pygame.Rect]:
		return collision_walls + [pygame.Rect(*sprite.position, sprite.side, sprite.side)
		                          for sprite in self.sprites.list_of_objects if sprite.is_blocked]

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
		self.mouse_control()
		self.rect.center = self.position
		self.angle %= DOUBLE_PI

	def key_control(self) -> None:
		sin_a, cos_a = sin(self.angle), cos(self.angle)
		keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

		# Exit
		if keys[pygame.K_ESCAPE]:
			exit()

		# Move
		if keys[pygame.K_w]:  # Forward
			dx = PLAYER_SPEED * cos_a
			dy = PLAYER_SPEED * sin_a
			self.detect_collision(dx, dy)

		if keys[pygame.K_s]:  # Backward
			dx = -PLAYER_SPEED * cos_a
			dy = -PLAYER_SPEED * sin_a
			self.detect_collision(dx, dy)

		if keys[pygame.K_a]:  # Left
			dx = PLAYER_SPEED * sin_a
			dy = -PLAYER_SPEED * cos_a
			self.detect_collision(dx, dy)

		if keys[pygame.K_d]:  # Right
			dx = -PLAYER_SPEED * sin_a
			dy = PLAYER_SPEED * cos_a
			self.detect_collision(dx, dy)

		# Rotate
		if keys[pygame.K_LEFT]:  # Left
			self.angle -= PLAYER_ROTATION_SPEED

		if keys[pygame.K_RIGHT]:  # Right
			self.angle += PLAYER_ROTATION_SPEED

		# Other
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and not self.shot:
					self.shot = True

	def mouse_control(self) -> None:
		if pygame.mouse.get_focused():
			difference: int = pygame.mouse.get_pos()[0] - HALF_WIDTH
			pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
			self.angle += difference * PLAYER_MOUSE_SENSITIVITY
