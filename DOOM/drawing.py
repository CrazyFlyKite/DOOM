from collections import deque
from math import sin, cos, degrees

import pygame

from map import mini_map
from player import Player
from utilities import *


class Drawing:
	def __init__(self, screen: Surface, screen_map: Surface, player: Player) -> None:
		self.screen = screen
		self.screen_map = screen_map
		self.player = player
		self.font = pygame.font.SysFont('Arial', 30, bold=True)
		self.textures = {
			WALL1: pygame.image.load('../assets/images/wall 1.png').convert(),
			WALL2: pygame.image.load('../assets/images/wall 2.png').convert(),
			WALL3: pygame.image.load('../assets/images/wall 3.png').convert(),
			WALL4: pygame.image.load('../assets/images/wall 4.png').convert(),
			SKY: pygame.image.load('../assets/images/sky.png').convert()
		}

		# Player weapon
		self.weapon_base_sprite = pygame.image.load('../assets/sprites/weapons/shotgun/base/0.png').convert_alpha()
		self.weapon_shot_animation = deque([
			pygame.image.load(f'../assets/sprites/weapons/shotgun/shot/{i}.png').convert_alpha() for i in range(20)
		])
		self.weapon_rect = self.weapon_base_sprite.get_rect()
		self.weapon_position = HALF_WIDTH - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height
		self.shot_length = len(self.weapon_shot_animation)
		self.shot_length_count = 0
		self.shot_animation_speed = 3
		self.shot_animation_count = 0
		self.shot_animation_trigger = True

		# SFX
		self.sfx = deque([
			pygame.image.load(f'../assets/sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(9)
		])
		self.sfx_length_count = 0
		self.sfx_length = len(self.sfx)

		# Defaults
		self.shot_projection = 0

	def background(self, angle: float) -> None:
		sky_offset: float = -5 * degrees(angle) % WIDTH
		self.screen.blit(self.textures[SKY], (sky_offset, 0))
		self.screen.blit(self.textures[SKY], (sky_offset - WIDTH, 0))
		self.screen.blit(self.textures[SKY], (sky_offset + WIDTH, 0))
		pygame.draw.rect(self.screen, DARK_GRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

	def world(self, world_objects: Walls) -> None:
		for obj in sorted(world_objects, key=lambda x: x[0], reverse=True):
			if obj[0]:
				_, object_, object_position = obj
				self.screen.blit(object_, object_position)

	def fps(self, clock: pygame.time.Clock) -> None:
		self.screen.blit(self.font.render(str(int(clock.get_fps())), 0, DARK_ORANGE), FPS_LABEL_POSITION)

	def mini_map(self, player: Player) -> None:
		self.screen_map.fill(BLACK)
		map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
		pygame.draw.line(self.screen_map, YELLOW, (map_x, map_y),
		                 (map_x + 12 * cos(player.angle), map_y + 12 * sin(player.angle)), 3)
		pygame.draw.circle(self.screen_map, RED, (map_x, map_y), 5)

		for x, y in mini_map:
			pygame.draw.rect(self.screen_map, DARK_BROWN, (x, y, MAP_TILE, MAP_TILE))

		self.screen.blit(self.screen_map, MAP_POSITION)

	def player_weapon(self, shots: List[Position | int]) -> None:
		if self.player.shot:
			self.shot_projection = min(shots)[1] // 2
			self.bullet_sfx()

			shot_sprite: Surface = self.weapon_shot_animation[0]
			self.screen.blit(shot_sprite, self.weapon_position)
			self.shot_animation_count += 1

			if self.shot_animation_count == self.shot_animation_speed:
				self.weapon_shot_animation.rotate(-1)
				self.shot_animation_count = 0
				self.shot_length_count += 1
				self.shot_animation_trigger = False

			if self.shot_length_count == self.shot_length:
				self.player.shot = False
				self.shot_length_count = 0
				self.sfx_length_count = 0
				self.shot_animation_trigger = True
		else:
			self.screen.blit(self.weapon_base_sprite, self.weapon_position)

	def bullet_sfx(self) -> None:
		if self.sfx_length_count < self.sfx_length:
			sfx: Surface = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
			sfx_rect: pygame.Rect = sfx.get_rect()
			self.screen.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
			self.sfx_length_count += 1
			self.sfx.rotate(-1)
