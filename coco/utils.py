import os
import json
import shutil


def detect_classes(annotation_path):
    classes = set()
    for anno_file in os.listdir(annotation_path):
        categories = json.load(open(os.path.join(annotation_path, anno_file), 'r', encoding='utf-8'))["categories"]
        for c in categories:
            classes.add(c["name"])
    return list(classes)


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] + box[2] / 2.0
    y = box[1] + box[3] / 2.0
    w = box[2]
    h = box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x = round(x,6)
    w = round(w,6)
    y = round(y,6)
    h = round(h,6)
    return (x, y, w, h)

def create_image(src, dst, mode):
    if mode == "copy":
        shutil.copy(src, dst)
    elif mode == "cut":
        shutil.move(src, dst)
    else:
        raise NotImplementedError("MODE must be 'copy' or 'cut'")