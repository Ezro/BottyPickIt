from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum


@dataclass_json
@dataclass
class ItemQuality(Enum):
    Normal = 'normal'
    Magic = 'magic'
    Rare = 'rare'
    Set = 'set'
    Unique = 'unique'
    Crafted = 'crafted'
