from typing import Dict, Set, Optional

import numpy as np

from utilities import *


# Level map
def load_map(map_file: PathLikeString, separator: Optional[str] = ' ') -> np.ndarray:
	try:
		with open(map_file, 'r', encoding='utf-8') as file:
			return np.array(
				[
					[
						int(number) if number != '_' else 0 for number in line.strip().split(separator)
					] for line in file.readlines()
				]
			)
	except OSError:
		return np.zeros(shape=(1, 1))


# Fill
map_array: np.ndarray = load_map(MAP_FILE)
WORLD_WIDTH: Final[int] = len(map_array[0]) * TILE
WORLD_HEIGHT: Final[int] = len(map_array) * TILE
world_map: Dict[Position, ElementType] = {}
mini_map: Set[Position] = set()

for j, row in enumerate(map_array):
	for i, item in enumerate(row):
		if item:
			mini_map.add((i * MAP_TILE, j * MAP_TILE))

			if item == 1:
				world_map[(i * TILE, j * TILE)] = ElementType.WALL1
			elif item == 2:
				world_map[(i * TILE, j * TILE)] = ElementType.WALL2
			elif item == 3:
				world_map[(i * TILE, j * TILE)] = ElementType.WALL3
			elif item == 4:
				world_map[(i * TILE, j * TILE)] = ElementType.WALL4
