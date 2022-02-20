
from item.base_items import BaseItem
from item.item_quality import ItemQuality
import screen
import cv2
import keyboard
import os
from bot import application_path
from item.item_finder import ItemFinder
from vision import draw_output_onto_image, whats_on_the_screen, pretty_print_output
import time

keyboard.add_hotkey('f12', lambda: os._exit(1))

debug_line_map = {}
debug_line_map[ItemQuality.Normal.value] = (208, 208, 208)
debug_line_map[ItemQuality.Magic.value] = (178, 95, 95)
debug_line_map[ItemQuality.Rare.value] = (107, 214, 214)
debug_line_map[ItemQuality.Set.value] = (0, 238, 0)
debug_line_map[ItemQuality.Unique.value] = (126, 170, 184)
debug_line_map[ItemQuality.Crafted.value] = (0, 160, 219)

if __name__ == "__main__":
    item_finder = ItemFinder()
    test_path = os.path.join(application_path, 'test_rings_and_sacred_armors.png')
    image = cv2.imread(test_path)
    # whats_on_the_screen(image)
    # ===
    # Vision Debug
    # ===
    # output = whats_on_the_screen(image)
    # # pretty_print_output(output)
    # cv2.imshow('image', image)
    # cv2.waitKey()
    # ===
    # Manual Debug calling item_finder
    # ===
    # ring_item_list = item_finder.search_for_base_item(image, BaseItem.Ring)
    # armor_item_list = item_finder.search_for_base_item(image, BaseItem.SacredArmor)
    # for item in ring_item_list:
    #     cv2.circle(image, item.center, 5, (255, 0, 255), thickness=3)
    # for item in armor_item_list:
    #     cv2.circle(image, item.center, 5, (255, 0, 255), thickness=3)
    #     # cv2.rectangle(image, item.roi[:2], (item.roi[0] + item.roi[2], item.roi[1] + item.roi[3]), (0, 0, 255), 1)
    # cv2.imshow('image', image)
    # cv2.waitKey()
    # ===
    # Live Debug
    # ===
    # keyboard.wait("f11")
    # while 1:
    #     image = screen.grab().copy()
    #     ring_item_list = search_for_base_item(image, BaseItem.Ring)
    #     armor_item_list = search_for_base_item(image, BaseItem.SacredArmor)
    #     for item in ring_item_list:
    #         cv2.circle(image, item.center, 5, (255, 0, 255), thickness=3)
    #     for item in armor_item_list:
    #         cv2.circle(image, item.center, 5, (255, 0, 255), thickness=3)
    #     cv2.rectangle(image, item.roi[:2], (item.roi[0] + item.roi[2], item.roi[1] + item.roi[3]), (0, 0, 255), 1)
    #     cv2.imshow('image', image)
    #     cv2.waitKey(1)
    #     output_path = os.path.join(application_path, 'screenshot.png')
    #     cv2.imwrite(output_path, image)
    # ===
    # Live Debug using Vision
    # ===
    keyboard.wait("f11")
    while 1:
        image = screen.grab().copy()
        start = time.time()
        output = whats_on_the_screen(image)
        draw_output_onto_image(image, output)
        end = time.time()
        elapsed = end - start
        print(f'What\'s on finished in {elapsed} seconds')
        # ring_item_list = search_for_base_item(image, BaseItem.Ring)
        # armor_item_list = search_for_base_item(image, BaseItem.SacredArmor)
        # for item in ring_item_list:
        #     cv2.circle(image, item.center, 5, (255, 0, 255), thickness=3)
        # for item in armor_item_list:
        #     cv2.circle(image, item.center, 5, (255, 0, 255), thickness=3)
        # cv2.rectangle(image, item.roi[:2], (item.roi[0] + item.roi[2], item.roi[1] + item.roi[3]), (0, 0, 255), 1)
        cv2.imshow('image', image)
        cv2.waitKey(1)
        # output_path = os.path.join(application_path, 'screenshot.png')
        # cv2.imwrite(output_path, image)
