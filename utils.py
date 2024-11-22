# -*- coding: utf-8 -*-
import os
import random
import shutil
import xml.etree.ElementTree as ET


# TODO 自动检测所有标签 保存为classes文件
def detect_classes(annotation_path):
    pass

# TODO 文件名和id映射(file, id) 修改文件名
def split_dataset(annotation_path, ratio):
    # TODO 过滤掉非xml文件
    total_xml = os.listdir(annotation_path)

    total_num = len(total_xml)
    sets_num = [int(r*total_num) for r in ratio]

    current_set = set(range(total_num))
    filtered_set = []
    for idx, n in enumerate(sets_num):
        if idx == len(sets_num)-1:
            filtered_set.append(list(current_set))
            break
        selected_set = random.sample(list(current_set), k=n)
        current_set -= set(selected_set)
        filtered_set.append(selected_set)

    # print([len(x) for x in filtered_set], total_num)

    return filtered_set

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

    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in all_classes or int(difficult) == 1:
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

        labels.append(f"{str(cls_id)} {" ".join([str(a) for a in bb])}\n")

    return labels

def create_image(src, dst, mode):
    if mode == "copy":
        shutil.copy(src, dst)
    elif mode == "cut":
        shutil.move(src, dst)
    else:
        raise NotImplementedError("MODE must be 'copy' or 'cut'")