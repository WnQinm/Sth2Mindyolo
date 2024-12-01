import os
import json
from tqdm.auto import tqdm
from .Params import Param
from .utils import *


def coco2yolo(**kwargs):
    P = Param(**kwargs)

    for set_name in P.Set_names:
        label_path = os.path.join(P.anno_path, f"instance_{set_name}.json")
        img_path = os.path.join(P.Dataset_PATH, set_name)
        output_img_path = os.path.join(P.output_img_path, set_name)
        output_label_path = os.path.join(P.output_label_path, set_name)

        data = json.load(open(label_path, 'r', encoding='utf-8'))
        images = {
            img["id"]: {
                "file_name": img["file_name"],
                "width": img["width"],
                "height": img["height"],
                "labels": []
            }
            for img in data["images"]
        }
        label_id2name = {c["id"]:c["name"] for c in data["categories"]}

        for ann in data["annotations"]:
            image_id = ann["image_id"]
            bbox = ann["bbox"]
            label = P.Classes[label_id2name[ann["category_id"]]]
            img_width = images[image_id]["width"]
            img_height = images[image_id]["height"]

            box = convert((img_width, img_height), bbox)
            images[image_id]["labels"].append(f"{label} {box[0]} {box[1]} {box[2]} {box[3]}\n")

        used_data = []
        for img_id, img_data in tqdm(images.items(), desc=f"creating {set_name} dataset"):
            with open(os.path.join(output_label_path, f"{img_id}.txt"), 'w', encoding='utf-8') as f:
                f.writelines(img_data["labels"])
            create_image(
                os.path.join(img_path, img_data["file_name"]),
                os.path.join(output_img_path, f"{img_id}.jpg"),
                P.MODE,
            )
            used_data.append(f"./images/{set_name}/{img_id}.jpg\n")
        with open(os.path.join(P.Output_PATH, f"{set_name}.txt"), 'w', encoding='utf-8') as f:
            f.writelines(used_data)
