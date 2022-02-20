from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

@dataclass_json
@dataclass
class Rune(Enum):
    Jah = "JAH"
    Ith = "ITH"
    Ber = "BER"