# What do you see on screen?
from item.base_items import BaseItem
from item.item_quality import ItemQuality
from item.item_finder import ItemFinder
import cv2
from botty_pickit import BOTTY_ITEMS_BY_BASE_THEN_QUALITY as botty_items

item_finder = ItemFinder()

debug_line_map = {}
debug_line_map[ItemQuality.Normal.value] = (208, 208, 208)
debug_line_map[ItemQuality.Magic.value] = (178, 95, 95)
debug_line_map[ItemQuality.Rare.value] = (107, 214, 214)
debug_line_map[ItemQuality.Set.value] = (0, 238, 0)
debug_line_map[ItemQuality.Unique.value] = (126, 170, 184)
debug_line_map[ItemQuality.Crafted.value] = (0, 160, 219)

def whats_on_the_screen(image):
    items_on_floor = []
    for base_item in botty_items:
        for quality in botty_items[base_item]:
            if base_item == 'ring':
                # items_on_floor.extend(botty_items[base_item][quality].scan_image_for_ground_ref(image))
                items_on_floor.extend(item_finder.search_for_base_item_and_quality(
                    image,
                    BaseItem(base_item),
                    ItemQuality(quality)))
    # items_on_floor.extend(item_finder.search_for_base_item_and_quality(image, BaseItem.Ring, ItemQuality.Unique))
    # items_on_floor.extend(item_finder.search_for_base_item(image, BaseItem.SacredArmor))
    distinct_items_on_floor = get_distinct_items_on_floor(items_on_floor, image)
    return build_output_from_items_on_floor(distinct_items_on_floor)

def get_distinct_items_on_floor(items_on_floor, image):
    distinct_items_on_floor = []
    for item_on_floor in items_on_floor:
        if not item_on_floor in distinct_items_on_floor:
            distinct_items_on_floor.append(item_on_floor)
    for item_on_floor in distinct_items_on_floor:
        # print(item_on_floor.baseItem, item_on_floor.quality, item_on_floor.center)
        cv2.rectangle(
            image,
            item_on_floor.roi[:2],
            (item_on_floor.roi[0] + item_on_floor.roi[2], item_on_floor.roi[1] + item_on_floor.roi[3]),
            debug_line_map[item_on_floor.quality],
            1
        )
        # cv2.circle(
        #     image,
        #     item_on_floor.center,
        #     5,
        #     debug_line_map[item_on_floor.quality],
        #     thickness=2
        # )
        # cv2.imshow('image', image)
        # cv2.waitKey()
    return distinct_items_on_floor

def build_output_from_items_on_floor(items_on_floor):
    output = {}
    if len(items_on_floor) == 0:
        return None
    for item in items_on_floor:
        output_item = {
            'center': item.center,
            'roi': item.roi
        }
        if not item.baseItem in output:
            output[item.baseItem] = {}
        if not item.quality in output[item.baseItem]:
            output[item.baseItem][item.quality] = []
        output[item.baseItem][item.quality].append(output_item)
    return output

def draw_output_onto_image(image, output):
    if not output:
        return
    for base_item in output:
        for quality in output[base_item]:
            for found_item in output[base_item][quality]:
                roi = found_item['roi']
                cv2.rectangle(
                    image,
                    roi[:2],
                    (roi[0] + roi[2], roi[1] + roi[3]),
                    debug_line_map[quality],
                    1
                )

def pretty_print_output(output):
    for base_item in output:
        for quality in output[base_item]:
            print(f'Detected {len(output[base_item][quality])} {quality} {base_item}s')