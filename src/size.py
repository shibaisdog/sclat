import cv2
import numpy as np

def sizeup(frame, new_size):
    h, w = frame.shape[:2]
    new_width = new_size[0]
    new_height = new_size[1]
    aspect_ratio = w / h
    target_height = new_height
    target_width = int(target_height * aspect_ratio)
    if target_width < new_width:
        target_width = new_width
        target_height = int(target_width / aspect_ratio)
    resized_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    if target_width < new_width:
        padding_left = (new_width - target_width) // 2
        padding_right = new_width - target_width - padding_left
        resized_frame = cv2.copyMakeBorder(resized_frame, 0, 0, padding_left, padding_right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    if target_height < new_height:
        padding_top = (new_height - target_height) // 2
        padding_bottom = new_height - target_height - padding_top
        resized_frame = cv2.copyMakeBorder(resized_frame, padding_top, padding_bottom, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    resized_frame = np.rot90(resized_frame, 3)
    resized_frame = cv2.flip(resized_frame, 1)
    return cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)