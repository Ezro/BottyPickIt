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
The current design aims to replace the items aspect of the TemplateFinder; rather than placing items into assets/items, the thinking is that reference images (as well as pickit overrides) would reside in a base_items/{base_item} folder.

### TemplateFinder Items Replacement
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