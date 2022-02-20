from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

@dataclass_json
@dataclass
class BaseItem(Enum):
    Ring = 'ring'
    Tiara = 'tiara'
    SacredArmor = 'sacred armor'