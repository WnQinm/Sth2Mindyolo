# -*- coding: utf-8 -*-
import os
import re
import random
import shutil
import xml.etree.ElementTree as ET


def detect_classes(annotation_path, classes_path=None) -> list[str]:
    if classes_path:
        print(f"use {classes_path}")
        return [c.replace("\n", "") for c in open(classes_path, "r", encoding="utf-8").readlines()]
    classes = set()
    for file in os.listdir(annotation_path):
        if file.endswith("xml"):
            tree = ET.parse(os.path.join(annotation_path, file))
            root = tree.getroot()
            for obj in root.iter('object'):
                cls_name = obj.find('name').text
                cls_name = re.sub(" ", "", cls_name)
                classes.add(cls_name)
    return list(classes)

def split_dataset(annotation_path, set_names, set_ratios) -> list:
    total_xml = [file.replace(".xml", "") for file in os.listdir(annotation_path) if file.endswith("xml")]

    total_num = len(total_xml)
    sets_num = [int(r*total_num) for r in set_ratios]

    for name, num in zip(set_names, sets_num):
        if num <= 0:
            print(f"\033[1;31m[WARNING]:\033[0m {name}数据集所含数据量为0")

    current_set = set(range(total_num))
    filtered_set = []
    filtered_set_id = []
    for idx, n in enumerate(sets_num):
        if idx == len(sets_num)-1:
            filtered_set.append([total_xml[i] for i in list(current_set)])
            filtered_set_id.append(list(current_set))
            break
        selected_set = random.sample(list(current_set), k=n)
        current_set -= set(selected_set)
        filtered_set.append([total_xml[i] for i in selected_set])
        filtered_set_id.append(selected_set)

    return filtered_set, filtered_set_id

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x = round(x,6)
    w = round(w,6)
    y = round(y,6)
    h = round(h,6)
    return x, y, w, h

def get_labels(xml_file_path, all_classes):
    labels = []

    with open(xml_file_path, "r", encoding="utf-8") as f:
        tree = ET.parse(f)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w==0 or h==0:
        return False

    for obj in root.iter('object'):
        difficult = int(obj.find('difficult').text)
        cls = obj.find('name').text
        if cls not in all_classes or difficult == 1:
            continue
        cls_id = all_classes.index(cls)

        xmlbox = obj.find('bndbox')
        b1 = float(xmlbox.find('xmin').text)
        b2 = float(xmlbox.find('xmax').text)
        b3 = float(xmlbox.find('ymin').text)
        b4 = float(xmlbox.find('ymax').text)
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)

        labels.append(f"{str(cls_id)} {' '.join([str(a) for a in bb])}\n")

    return labels

def create_image(src, dst, mode):
    if mode == "copy":
        shutil.copy(src, dst)
    elif mode == "cut":
        shutil.move(src, dst)
    else:
        raise NotImplementedError("MODE must be 'copy' or 'cut'")