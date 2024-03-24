from math import tan, pi
from os import PathLike
from typing import Tuple, Final, TypeAlias

# Custom types
Number: TypeAlias = int | float
Position: TypeAlias = Tuple[Number, Number]
Color: TypeAlias = Tuple[int, int, int]
PathLikeString: TypeAlias = str | bytes | PathLike

# Main map
WIDTH: Final[int] = 1200
HEIGHT: Final[int] = 800
HALF_WIDTH: Final[int] = WIDTH // 2
HALF_HEIGHT: Final[int] = HEIGHT // 2
FPS_POSITION: Final[Position] = WIDTH - 50, 5
TILE: Final[int] = 100
FPS: Final[int] = 60

# Mini map
MAP_SCALE: Final[int] = 5
MAP_TILE: Final[int] = TILE // MAP_SCALE
MAP_POSITION: Final[Position] = 0, HEIGHT - HEIGHT // MAP_SCALE
MAP_WIDTH: Final[int] = WIDTH // MAP_SCALE
MAP_HEIGHT: Final[int] = HEIGHT // MAP_SCALE

# Player
PLAYER_POSITION: Position = HALF_WIDTH, HALF_HEIGHT
PLAYER_ANGLE: Final[float] = 0.0
PLAYER_SPEED: Final[int] = 2

# Ray casting
FOV: Final[float] = pi / 3
HALF_FOV: Final[float] = FOV / 2
NUMBER_RAYS: Final[int] = 300
MAX_DEPTH: Final[int] = 800
DELTA_ANGLE: Final[float] = FOV / NUMBER_RAYS
DIST: Final[float] = NUMBER_RAYS / (2 * tan(HALF_FOV))
PROJECTION_COEFFICIENT: Final[float] = 3 * DIST * TILE
SCALE: Final[int] = WIDTH // NUMBER_RAYS

# Game elements
WALL1: Final[str] = '1'
WALL2: Final[str] = '2'
SKY: Final[str] = 'sky'

# Texture settings
TEXTURE_WIDTH: Final[int] = 1200
TEXTURE_HEIGHT: Final[int] = 1200
TEXTURE_SCALE: Final[int] = TEXTURE_WIDTH // TILE

# FILES
MAP_FILE: Final[PathLikeString] = '../assets/map.txt'
TEXTURE1: Final[PathLikeString] = '../assets/images/texture 1.png'
TEXTURE2: Final[PathLikeString] = '../assets/images/texture 2.png'
TEXTURE_SKY: Final[PathLikeString] = '../assets/images/sky.png'

# Colors
RED: Final[Color] = 220, 0, 0
YELLOW: Final[Color] = 220, 220, 0
SANDY: Final[Color] = 244, 164, 96
GREEN: Final[Color] = 0, 80, 0
SKY_BLUE: Final[Color] = 0, 186, 255
DARK_GRAY: Final[Color] = 110, 110, 110
BLACK: Final[Color] = 0, 0, 0
