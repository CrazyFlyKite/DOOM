from dataclasses import dataclass
from enum import Enum
from math import tan, pi
from os import PathLike
from typing import List, Tuple, Deque, Final, TypeAlias

from pygame import Surface

# Custom types
Number: TypeAlias = int | float
Position: TypeAlias = Tuple[Number, Number]
Surfaces: TypeAlias = List[Surface]
Wall: TypeAlias = Tuple[float, Surface, Position]
Walls: TypeAlias = List[Wall]
Color: TypeAlias = Tuple[int, int, int]
PathLikeString: TypeAlias = str | bytes | PathLike

# Main map
WIDTH: Final[int] = 1200
HEIGHT: Final[int] = 800
HALF_WIDTH: Final[int] = WIDTH // 2
HALF_HEIGHT: Final[int] = HEIGHT // 2
PENTA_HEIGHT: Final[int] = HEIGHT * 5
DOUBLE_HEIGHT: Final[int] = HEIGHT * 2

TILE: Final[int] = 100

FPS_LABEL_POSITION: Final[Position] = WIDTH - 50, 5
FPS: Final[int] = 60
MAP_FILE: Final[PathLikeString] = '../assets/data/map.txt'

# Mini map
MINIMAP_SCALE: Final[int] = 5
MINIMAP_RESOLUTION: Final[Position] = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE: Final[int] = 2 * MINIMAP_SCALE
MAP_TILE: Final[int] = TILE // MAP_SCALE
MAP_POSITION: Final[Position] = 0, HEIGHT - HEIGHT // MINIMAP_SCALE
MAP_WIDTH: Final[int] = WIDTH // MAP_SCALE
MAP_HEIGHT: Final[int] = HEIGHT // MAP_SCALE

# Player
PLAYER_POSITION: Position = HALF_WIDTH // 4, HALF_HEIGHT
PLAYER_ANGLE: Final[float] = 0
PLAYER_SPEED: Final[int] = 3
PLAYER_ROTATION_SPEED: Final[float] = 0.03
PLAYER_MOUSE_SENSITIVITY: Final[float] = 0.003

# Ray casting
FOV: Final[float] = pi / 3
HALF_FOV: Final[float] = FOV / 2
NUMBER_RAYS: Final[int] = 300
MAX_DEPTH: Final[int] = 800
DELTA_ANGLE: Final[float] = FOV / NUMBER_RAYS
DIST: Final[float] = NUMBER_RAYS / (2 * tan(HALF_FOV))
PROJECTION_COEFFICIENT: Final[float] = 3 * DIST * TILE
SCALE: Final[int] = WIDTH // NUMBER_RAYS

# Texture settings
TEXTURE_WIDTH: Final[int] = 1200
TEXTURE_HEIGHT: Final[int] = 1200
TEXTURE_SCALE: Final[int] = TEXTURE_WIDTH // TILE


# Texture types
class ElementType(Enum):
	VOID = 'void'
	WALL1 = 'wall1'
	WALL2 = 'wall2'
	WALL3 = 'wall3'
	WALL4 = 'wall4'
	SKY = 'sky'


# Sprite settings
DOUBLE_PI: Final[float] = pi * 2
CENTER_RAY: Final[int] = NUMBER_RAYS // 2 - 1
FAKE_RAYS: Final[int] = 100
FAKE_RAYS_RANGE: Final[int] = NUMBER_RAYS - 1 + 2 * FAKE_RAYS


# Sprite types
class SpriteType:
	BARREL = 'barrel'
	PIN = 'pin'
	DEVIL = 'devil'
	FLAME = 'flame'


# Sprite parameters
@dataclass(frozen=True)
class SpriteParameters:
	sprite: Surface | Surfaces
	viewing_angles: bool
	shift: float
	scale: float
	animation: Deque[Surface]
	animation_dist: int
	animation_speed: int
	blocked: bool


# Colors
RED: Final[Color] = 220, 0, 0
DARK_ORANGE: Final[Color] = 255, 140, 0
YELLOW: Final[Color] = 220, 220, 0
DARK_BROWN: Final[Color] = 97, 61, 25
DARK_GRAY: Final[Color] = 110, 110, 110
BLACK: Final[Color] = 0, 0, 0
