from typing import Dict, Set, Optional

import pygame
from numba import int32
from numba.core.types import UniTuple
from numba.typed.typeddict import Dict as NumbaDict

from utilities import *


# Get map function
def load_map(map_file: PathLikeString, separator: Optional[str] = ' ') -> List[List[int]]:
	mapping: Dict[str, int] = {
		'_': VOID,
		'1': WALL1,
		'2': WALL2,
		'3': WALL3,
		'4': WALL4
	}

	with open(map_file, 'r', encoding='utf-8') as file:
		return [[mapping.get(character) for character in line.strip().split(separator)] for line in file.readlines()]


# Initialize
map_array: List[List[int]] = load_map(MAP_FILE)
WORLD_WIDTH: Final[int] = len(map_array[0]) * TILE
WORLD_HEIGHT: Final[int] = len(map_array) * TILE

# Maps
world_map: NumbaDict = NumbaDict.empty(key_type=UniTuple(int32, 2), value_type=int32)
mini_map: Set[Position] = set()
collision_walls: List[pygame.Rect] = []

# Fill
for j, row in enumerate(map_array):
	for i, item in enumerate(row):
		if item != VOID:
			mini_map.add((i * MAP_TILE, j * MAP_TILE))
			collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
			world_map[(i * TILE, j * TILE)] = item
