# Botty PickIt

## Design Goals
* Be able to provide Botty with "eyes" (vision module) / "brains" (loot detector)
* Be able to answer the following questions:
    ```
    - Is there any loot on the ground?
    - Is any of the loot worth picking up?
    - Is any of the picked up loot worth keeping?
    - What identifiable items are on the screen?
        - Are there tomes of TP / ID or cube in the inventory?
        - Are those glaives worth checking for BO? (Claws for trap?)
        - How many transmutes are available?
    ```
## Implementation Details
### TemplateFinder Items Replacement
The current design aims to replace the items aspect of the TemplateFinder; rather than placing items into assets/items, the thinking is that reference images (as well as pickit overrides) would reside in a base_items/{base_item} folder.
e.g.,
```
/base_items/ring/magic.png
/base_items/ring/rare.png
/base_items/ring/set.png
/base_items/ring/crafted.png
/base_items/ring/unique.png
```
These files represent the "groundRef" (reference image when the item is on the ground) of the quality + base_item (e.g., rare ring). The reason I think is so beneficial is because it would be much easier to identify which items can be recognized and which would be ignored.

In addition to the keyworded files that represent quality (magic, rare, etc.), reference files can also be included for identifying the base_item when looking at the inventory / stash / shop, etc.

e.g.,
```
/base_items/ring/ref1.png
```
Any file starting with ref would be added to a list of 'refs'.

Both the base_item's groundRef as well as refs would be gathered at startup and used within the "vision module".

### PickIt
The goal of the new PickIt system is to be able to drive the loot configuration in a mode user-friendly way. The new approach highlighted in this repo has the following:

* Consolidated pickit rules in a loot_pickit.json file
* Allow for overrides via loot_pickit_override.json files within the base_items folders

e.g.,
```json
# loot_pickit.json
[{
        "baseItem": "ring",
        "quality": "rare",
        "pickUp": true,
        "id": true,
        "sell": false,
        "keepIf": [
            "fcr=10 & (str >= 20 | str+dex >= 15 & (maxHp >= 30 | maxMana >= 60) | maxHp >= 30 & maxMana >= 60)"
        ]
    }
]

# base_item/ring/loot_pickit_override.json
[{
    "quality": "rare",
    "pickUp": true,
    "id": true,
    "sell": false,
    "keepIf": [
        "fcr=10",
        "lifeLeech > 4 & manaLeech > 4"
    ]
}, {
    "quality": "magic",
    "pickUp": true,
    "id": true,
    "sell": false,
    "keepIf": [
        "lifeLeech > 4 & manaLeech > 4"
    ]
}]
```
With the following setup, the default pickit rule is saying to look for a ring with 10fcr and a bunch of other stats; this gets overridden by the ring/loot_pickit_override.json resulting in the actual rules being for:
```
rare ring: fcr 10 OR (lifeLeech > 4 AND manaLeech > 4)
&
magic ring: lifeLeech >4 AND manaLeech >4
```

This allows for powerful customization / flexibility. e.g., People can use / share loot_pickit.json files freely without affecting their custom overrides.

#### PickIt Syntax
The proposed syntax also differs from existing PickIt files (NIP or otherwise). The new rule(s) take the shape of json with the following properties:
* baseItem: BaseItem (e.g., SacredArmor, Ring)
* quality: ItemQuality (e.g., Normal, Magic, Rare, Crafted, Unique)
* pickUp: bool (default to true)
* id: bool (default to true)
* sell: bool (default to false)
* keepIf: list[str]

__Important__
```
baseItem is only available on the loot_pickit.json and is inferred by the direction structure when using the loot_pickit_override.json
```
The keepIf section is where things should get a bit more familiar; the goal is to be able to abstract the higher level decision making to easily answer the previously listed questions:
```
BottyItem.groundRef => "Is there any loot on the ground?"
BottyItem.rule.pickUp => "Is any of the loot worth picking up?"
BottyItem.rule.keepIf => "Is any of the picked up loot worth keeping?"
```

#### KeepIf Syntax
keepIf should operate using similar syntax as NIP or the current ini file but using different keywords:

e.g., current rare ring rule
```
[type] == ring && [quality] == rare # [fcr] == 10 && ([strength] >= 20 || [strength]+[dexterity] >= 15 && ([maxhp] >= 30 || [maxmana] >= 60) || [maxhp] >= 30 && [maxmana] >= 60)
```

e.g., proposed rare ring rule
```
fcr=10 & (str >= 20 | str+dex >= 15 & (maxHp >= 30 | maxMana >= 60) | maxHp >= 30 & maxMana >= 60)
```

The keywords available should map directly to the new item/d2item.py class:
```python
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
```
## Considerations
The first aspect of this for replacing the TemplateFinder for base_items may also be moot since the OCR branch should be able to detect item text (i.e., base_item) as well as the color (i.e., quality)
