from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from runes import Rune
from item_skills import ItemSkill
from item.base_items import BaseItem

@dataclass_json
@dataclass
class ChanceToCastTrigger(Enum):
    Attack = "attack"
    Striking = "striking"
    Struck = "struck"
    Die = "die"
    Kill = "kill"
    LevelUp = "level-up"

@dataclass_json
@dataclass
class ChanceToCast:
    chance: int
    skill: ItemSkill
    level: int
    trigger: ChanceToCastTrigger

@dataclass_json
@dataclass
class Charge:
    skill: ItemSkill
    level: int
    current: int
    max: int

@dataclass_json
@dataclass
# TODO: Finish fleshing out this OCR parse data model
# The member variables that exist here would correspond to the available keyword values in the pickit.json
class D2Item:
    name: str
    baseItem: BaseItem
    runes: list[Rune] = None
    allSkills: int = None
    amazonSkills: int = None
    assassinSkills: int = None
    barbarianSkills: int = None
    druidSkills: int = None
    necroSkills: int = None
    paladinSkills: int = None
    sorceressSkills: int = None
    allStats: int = None
    allRes: int = None
    lightRadius: int = None
    chanceToCast: list[ChanceToCast] = None
    charges: list[Charge] = None
