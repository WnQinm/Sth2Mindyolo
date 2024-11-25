# -*- coding: utf-8 -*-
from tqdm.auto import tqdm
from Params import P
from utils import *


# 按提供的比例分割数据集
Datasets, Dataset_ids = split_dataset(P.Annotation_PATH, P.Set_names, P.Set_ratios)

for dataset, dataset_id, set_name in zip(Datasets, Dataset_ids, P.Set_names):
    print(f"create {set_name} dataset...")

    used_data = []

    for file, file_id in tqdm(zip(dataset, dataset_id), total=len(dataset)):
        # 根据xml文件编写yolo格式的标签
        annotation_file = os.path.join(P.Annotation_PATH, f"{file}.xml")
        labels = get_labels(annotation_file, P.Classes)

        # 如果size中的宽或高标注为0, 则无法计算label，跳过该数据
        if not labels:
            continue
        used_data.append(file_id)

        # 保存标签到指定路径
        with open(os.path.join(P.Output_label_path, set_name, f"{file_id}.txt"), 'w', encoding='utf-8') as label_file:
            label_file.writelines(labels)

        # 复制/剪切图片到指定路径
        create_image(os.path.join(P.Image_PATH, f"{file}.jpg"), os.path.join(P.Output_image_path, set_name, f"{file_id}.jpg"), P.MODE)

    id2path = lambda data_id: re.sub(r"\\{1,2}", "/", os.path.join("./images", set_name, f"{data_id}.jpg")+"\n")
    with open(os.path.join(P.Output_PATH, f"{set_name}.txt"), "w", encoding="utf-8") as f:
        f.writelines([id2path(d) for d in used_data])
