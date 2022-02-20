import sys
import os
from item import BaseItem, ItemQuality

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

REFS = {}

base_items_path = os.path.join(application_path, 'base_items')
for base_item_name in os.listdir(base_items_path):
    try:
        BaseItem(base_item_name)
        base_item_path = os.path.join(base_items_path, base_item_name)
        base_item_refs = []
        for file in os.listdir(base_item_path):
            file_full_path = os.path.join(base_item_path, file)
            if file.lower() == 'picker_override.json':
                continue
            else:
                if base_item_name not in REFS:
                    REFS[base_item_name] = {}
                if file.lower().endswith('png'):
                    if file.lower().startswith('ref'):
                        if 'refs' not in REFS[base_item_name]:
                            REFS[base_item_name]['refs'] = []
                        REFS[base_item_name]['refs'].append(file_full_path)
                    else:
                        filename = os.path.splitext(file)[0]
                        try:
                            if ItemQuality(filename):
                                if not filename in REFS[base_item_name]:
                                    REFS[base_item_name][filename] = {}
                                REFS[base_item_name][filename]['groundRef'] = file_full_path
                        except ValueError:
                            if not ItemQuality.Unique.value in REFS[base_item_name]:
                                REFS[base_item_name][ItemQuality.Unique.value] = {
                                    'refs': []
                                }
                            REFS[base_item_name][ItemQuality.Unique.value]['refs'].append(file_full_path)
    except ValueError:
        continue