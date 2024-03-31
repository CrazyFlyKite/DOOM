from typing import Dict, Set, Optional

from utilities import *


# Get map function
def load_map(map_file: PathLikeString, separator: Optional[str] = ' ') -> List[List[ElementType]]:
	mapping: Dict[str, ElementType] = {
		'_': ElementType.VOID,
		'1': ElementType.WALL1,
		'2': ElementType.WALL2,
		'3': ElementType.WALL3,
		'4': ElementType.WALL4
	}

	with open(map_file, 'r', encoding='utf-8') as file:
		return [[mapping.get(character) for character in line.strip().split(separator)] for line in file.readlines()]


# Initialize
map_array: List[List[ElementType]] = load_map(MAP_FILE)
WORLD_WIDTH: Final[int] = len(map_array[0]) * TILE
WORLD_HEIGHT: Final[int] = len(map_array) * TILE

# Maps
world_map: Dict[Position, ElementType] = {}
mini_map: Set[Position] = set()

# Fill
for j, row in enumerate(map_array):
	for i, item in enumerate(row):
		if item != ElementType.VOID:
			mini_map.add((i * MAP_TILE, j * MAP_TILE))
			world_map[(i * TILE, j * TILE)] = item
