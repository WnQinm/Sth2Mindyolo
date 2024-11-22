# -*- coding: utf-8 -*-
from tqdm.auto import tqdm
from Params import P
from utils import *


# 按提供的比例分割数据集
Datasets = split_dataset(P.Annotation_PATH, P.Set_ratio)
for dataset, set_name in tqdm(zip(Datasets, P.Sets_name)):
    print(f"create {set_name} dataset")
    for file, file_id in tqdm(dataset):
        # 根据xml文件编写yolo格式的标签
        with open(os.path.join(P.Annotation_PATH, f"{file}.xml"), "r", encoding='utf-8') as annotation_file:
            labels = get_labels(annotation_file, P.Classes)
        # 保存标签到指定路径
        with open(os.path.join(P.Output_label_path, set_name, f"{file_id}.txt"), 'w', encoding='utf-8') as label_file:
            label_file.writelines(labels)
        # 复制/剪切图片到指定路径
        create_image(os.path.join(P.Image_PATH, f"{file}.jpg"), os.path.join(P.Output_image_path, set_name, f"{file_id}.jpg"), P.MODE)
