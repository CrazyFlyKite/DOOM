from dataclasses import dataclass
from math import tan, pi
from os import PathLike
from typing import List, Tuple, Deque, Optional, Final, TypeAlias

from pygame import Surface

# Custom types
Number: TypeAlias = int | float
Position: TypeAlias = Tuple[Number, Number]
Scale: TypeAlias = Tuple[float, float]
Surfaces: TypeAlias = List[Surface]
Walls: TypeAlias = List[Tuple[float, Surface, Position]]
CastedWalls: TypeAlias = List[Tuple[float, int, int, int]]
Color: TypeAlias = Tuple[int, int, int]
PathLikeString: TypeAlias = str | bytes | PathLike

# Display
WIDTH: Final[int] = 1200
HEIGHT: Final[int] = 800
HALF_WIDTH: Final[int] = WIDTH // 2
HALF_HEIGHT: Final[int] = HEIGHT // 2
DOUBLE_HEIGHT: Final[int] = HEIGHT * 2
TILE: Final[int] = 100
FPS_LABEL_POSITION: Final[Position] = WIDTH - 50, 5
FPS: Final[int] = 60

# Minimap
MINIMAP_SCALE: Final[int] = 5
MINIMAP_RESOLUTION: Final[Position] = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE: Final[int] = MINIMAP_SCALE * 2
MAP_TILE: Final[int] = TILE // MAP_SCALE
MAP_POSITION: Final[Position] = 0, HEIGHT - HEIGHT // MINIMAP_SCALE

# Player
PLAYER_POSITION: Position = HALF_WIDTH // 4, HALF_HEIGHT
PLAYER_ANGLE: Final[float] = 0
PLAYER_SPEED: Final[int] = 4
PLAYER_ROTATION_SPEED: Final[float] = 0.03
PLAYER_MOUSE_SENSITIVITY: Final[float] = 300
PLAYER_SIDE: Final[int] = 50

# Ray casting
FOV: Final[float] = pi / 3
HALF_FOV: Final[float] = FOV / 2
NUMBER_RAYS: Final[int] = 300
DELTA_ANGLE: Final[float] = FOV / NUMBER_RAYS
DIST: Final[float] = NUMBER_RAYS / (2 * tan(HALF_FOV))
PROJECTION_COEFFICIENT: Final[float] = 3 * DIST * TILE
SCALE: Final[int] = WIDTH // NUMBER_RAYS

# Textures settings
TEXTURE_SIZE: Final[int] = 1200
HALF_TEXTURE_SIZE: Final[int] = TEXTURE_SIZE // 2
TEXTURE_SCALE: Final[int] = TEXTURE_SIZE // TILE

# Texture types
VOID: Final[int] = 0
WALL1: Final[int] = 1
WALL2: Final[int] = 2
WALL3: Final[int] = 3
WALL4: Final[int] = 4
SKY: Final[int] = 5
MENU: Final[int] = 6

# Sprites settings
DOUBLE_PI: Final[float] = pi * 2
CENTER_RAY: Final[int] = NUMBER_RAYS // 2 - 1
FAKE_RAYS: Final[int] = 100
FAKE_RAYS_RANGE: Final[int] = NUMBER_RAYS - 1 + 2 * FAKE_RAYS


# Sprite types, flags and deaths enumerations
class SpriteType:
	BARREL: int = 0
	PIN: int = 1
	DEVIL: int = 2
	FLAME: int = 3
	SOLIDER: int = 4


class Flag:
	DECORATION: int = 0
	NPC: int = 1


class DeathType:
	MORTAL: None = None
	IMMORTAL: str = 'immortal'


# Dataclass for sprite parameters
@dataclass(frozen=True, order=True)
class SpriteParameters:
	sprite: Surface | Surfaces
	has_viewing_angles: bool
	shift: float
	scale: Scale
	side: int
	animation: Deque[Surface]
	animation_dist: Optional[int]
	animation_speed: int
	death_animation: Deque[Surface]
	death_type: Optional[str]
	death_shift: Optional[float]
	is_blocked: Optional[bool]
	flag: int
	object_action: Deque[Surface]


# Colors
RED: Final[Color] = 220, 0, 0
DARK_ORANGE: Final[Color] = 255, 140, 0
YELLOW: Final[Color] = 220, 220, 0
DARK_BROWN: Final[Color] = 97, 61, 25
LIGHT_GRAY: Final[Color] = 211, 211, 211
DARK_GRAY: Final[Color] = 110, 110, 110
BLACK: Final[Color] = 0, 0, 0
