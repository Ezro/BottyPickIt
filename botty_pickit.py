from dataclasses import dataclass, field
from typing import Tuple
from dataclasses_json import config, DataClassJsonMixin, dataclass_json
from item import BaseItem, ItemQuality
from refs import REFS
import os
import json
import cv2
from bot import application_path
import numpy as np
import time
from utils.misc import cut_roi

debug_line_map = {}
debug_line_map[ItemQuality.Normal.value] = (208, 208, 208)
debug_line_map[ItemQuality.Magic.value] = (178, 95, 95)
debug_line_map[ItemQuality.Rare.value] = (107, 214, 214)
debug_line_map[ItemQuality.Set.value] = (0, 238, 0)
debug_line_map[ItemQuality.Unique.value] = (126, 170, 184)
debug_line_map[ItemQuality.Crafted.value] = (0, 160, 219)

@dataclass
class FoundItem():
    baseItem: BaseItem
    quality: ItemQuality = None
    center: Tuple[float, float] = None
    roi: list[int] = None

    def __init__(self, base_item, quality, center, roi):
        self.baseItem = base_item
        self.quality = quality
        self.center = center
        self.roi = roi

@dataclass
class BottyLootRule(DataClassJsonMixin):
    baseItem: BaseItem = field(metadata=config(encoder=lambda x: x.value, decoder=BaseItem))
    quality: ItemQuality = field(metadata=config(encoder=lambda x: x.value, decoder=ItemQuality))
    pickUp: bool = True
    id: bool = True
    keepIf: list[str] = None

@dataclass_json
@dataclass
class BottyPickIt:
    groundRef: str
    refs: list[str] = None
    lootRule: BottyLootRule = None
    groundRefData = None
    minScore = 0.86

    def __init__(self, groundRef, refs, lootRule):
        self.groundRef = groundRef
        self.refs = refs
        self.lootRule = lootRule
        self.ground_ref_data = cv2.imread(self.groundRef)

    def scan_image_for_ground_ref(self, image: np.ndarray):
        from item.item_finder import ItemFinder
        base_item, quality = self.get_base_item_and_quality()
        return ItemFinder().search_for_base_item_and_quality(
            image,
            base_item,
            quality)

    def get_base_item_and_quality(self):
        if self.lootRule:
            return self.lootRule.baseItem, self.lootRule.quality
        folder = self.groundRef.split('\\')[-2]
        quality = self.groundRef.split('\\')[-1].split('.')[-2]
        try:
            base_item = BaseItem(folder)
            quality = ItemQuality(quality)
        except ValueError:
            quality = None
        return base_item, quality

    def scan_image_for_refs(self, image):
        print(self.refs)

def load_botty_items():
    loaded_ezpicker_rules = {}
    picker_file = json.load(open('loot_pickit.json'))
    for rule_dict in picker_file:
        rule = BottyLootRule.from_dict(rule_dict)
        if rule.baseItem.value not in loaded_ezpicker_rules:
            loaded_ezpicker_rules[rule.baseItem.value] = {}
            loaded_ezpicker_rules[rule.baseItem.value][rule.quality.value] = rule
    override_loot_rules(loaded_ezpicker_rules)
    wip_picker_dict = prepare_item_dict(loaded_ezpicker_rules)
    return build_botty_items(wip_picker_dict)

def override_loot_rules(loaded_loot_rules):
    base_items_path = os.path.join(application_path, 'base_items')
    for base_item_name in os.listdir(base_items_path):
        base_item_path = os.path.join(base_items_path, base_item_name)
        for file in os.listdir(base_item_path):
            file_full_path = os.path.join(base_item_path, file)
            if file.lower() == 'loot_pickit_override.json':
                picker_override_file = json.load(open(file_full_path))
                for rule in picker_override_file:
                    rule['baseItem'] = base_item_name
                    loaded_loot_rules[base_item_name][ItemQuality(rule['quality']).value] = BottyLootRule.from_dict(rule)

def prepare_item_dict(loaded_loot_rules):
    wip_picker_items = {}
    for base_item in loaded_loot_rules:
        for quality in loaded_loot_rules[base_item]:
            if base_item not in REFS or quality not in REFS[base_item]:
                # TODO: Throw?
                continue
            if base_item not in wip_picker_items:
                wip_picker_items[base_item] = {}
            if quality not in wip_picker_items[base_item]:
                wip_picker_items[base_item][quality] = {}
            if 'rule' not in wip_picker_items[base_item][quality]:
                wip_picker_items[base_item][quality]['rule'] = loaded_loot_rules[base_item][quality]
            wip_picker_items[base_item][quality]['groundRef'] = REFS[base_item][quality]['groundRef']
            if 'refs' in REFS[base_item][quality]:
                wip_picker_items[base_item][quality]['refs'] = REFS[base_item][quality]['refs']
    for base_item in REFS:
        for quality in REFS[base_item]:
            if quality == 'refs':
                continue
            if base_item not in wip_picker_items:
                wip_picker_items[base_item] = {}
            if quality not in wip_picker_items[base_item]:
                wip_picker_items[base_item][quality] = {}
            wip_picker_items[base_item][quality]['groundRef'] = REFS[base_item][quality]['groundRef']
            if 'refs' in REFS[base_item][quality]:
                wip_picker_items[base_item][quality]['refs'] = REFS[base_item][quality]['refs']
    return wip_picker_items

def build_botty_items(wip_item_dict):
    picker_items = {}
    for base_item in wip_item_dict:
        if base_item not in picker_items:
            picker_items[base_item] = {}
        for quality in wip_item_dict[base_item]:
            if quality not in picker_items[base_item]:
                picker_items[base_item][quality] = {}
            picker_item = BottyPickIt.from_dict(wip_item_dict[base_item][quality])
            picker_items[base_item][quality] = picker_item
    return picker_items

BOTTY_ITEMS_BY_BASE_THEN_QUALITY = load_botty_items()