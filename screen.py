import numpy as np
from mss import mss
import cv2
import time
from typing import Tuple
from utils.misc import find_d2r_window
import os
from config import Config

sct = mss()
monitor_roi = sct.monitors[0]
found_offsets = False
monitor_x_range = None
monitor_y_range = None

def convert_monitor_to_screen(screen_coord: Tuple[float, float]) -> Tuple[float, float]:
    global monitor_roi
    return (screen_coord[0] - monitor_roi["left"], screen_coord[1] - monitor_roi["top"])

def convert_screen_to_monitor(screen_coord: Tuple[float, float]) -> Tuple[float, float]:
    global monitor_roi
    x = screen_coord[0] + monitor_roi["left"]
    y = screen_coord[1] + monitor_roi["top"]
    return (np.clip(x, *monitor_x_range), np.clip(y, *monitor_y_range))

def convert_abs_to_screen(abs_coord: Tuple[float, float]) -> Tuple[float, float]:
    global monitor_roi
    # abs has it's center on char which is the center of the screen
    return ((monitor_roi["width"] // 2) + abs_coord[0], (monitor_roi["height"] // 2) + abs_coord[1])

def convert_screen_to_abs(screen_coord: Tuple[float, float]) -> Tuple[float, float]:
    global monitor_roi
    return (screen_coord[0] - (monitor_roi["width"] // 2), screen_coord[1] - (monitor_roi["height"] // 2))

def convert_abs_to_monitor(abs_coord: Tuple[float, float]) -> Tuple[float, float]:
    screen_coord = convert_abs_to_screen(abs_coord)
    monitor_coord = convert_screen_to_monitor(screen_coord)
    return monitor_coord

def set_window_position(offset_x: int, offset_y: int):
    global monitor_roi, monitor_x_range, monitor_y_range, found_offsets
    monitor_roi["top"] = offset_y
    monitor_roi["left"] = offset_x
    monitor_roi["width"] = Config().ui_pos["screen_width"]
    monitor_roi["height"] = Config().ui_pos["screen_height"]
    monitor_x_range = (monitor_roi["left"] + 10, monitor_roi["left"] + monitor_roi["width"] - 10)
    monitor_y_range = (monitor_roi["top"] + 10, monitor_roi["top"] + monitor_roi["height"] - 10)
    found_offsets = True

def grab() -> np.ndarray:
    global monitor_roi
    img = np.array(sct.grab(monitor_roi))
    return img[:, :, :3]

position = find_d2r_window()
if position is not None:
    set_window_position(*position)

if __name__ == "__main__":
    while 1:
        start = time.time()
        test_img = grab().copy()
        # print(time.time() - start)

        show_roi = True
        show_pt = True

        if show_roi:
            for roi_key in Config().ui_roi:
                x, y, w, h = Config().ui_roi[roi_key]
                # t = screen.convert_screen_to_monitor((0, 0))
                # p1 = screen.convert_screen_to_monitor((x, y))
                # p2 = screen.convert_screen_to_monitor((x+w, y+h))
                p1 = (x, y)
                p2 = (x+w, y+h)
                cv2.rectangle(test_img, p1, p2, (0, 255, 0), 2)
                cv2.putText(test_img, roi_key, (p1[0], p1[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

        if show_pt:
            pass

        cv2.imshow("test", test_img)
        cv2.waitKey(1)
