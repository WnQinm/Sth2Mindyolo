# -*- coding: utf-8 -*-
import os
import json
from typing import Union, List
from dataclasses import dataclass, field
from utils import detect_classes


@dataclass
class Param:
    Annotation_PATH: str = field(default="./Annotations")
    Image_PATH: str = field(default="./JPEGImages")
    Output_PATH: str = field(default="./output")

    Set_names: List[str] = field(default_factory=lambda: ["train", "val", "test"])
    Set_ratios: List[float] = field(default_factory=lambda: [0.8, 0.1, 0.1])
    Classes: Union[List[str], str] = field(default="auto")

    MODE: str = field(default="copy")

    def __post_init__(self):
        if not os.path.exists(self.Annotation_PATH) or len(os.listdir(self.Annotation_PATH))<=0:
            raise FileNotFoundError(f"无法找到Annotation_PATH, 或Annotation_PATH文件夹为空")
        if not os.path.exists(self.Image_PATH) or len(os.listdir(self.Image_PATH))<=0:
            raise FileNotFoundError(f"无法找到Image_PATH, 或Image_PATH文件夹为空")
        if os.path.exists(self.Output_PATH):
            if len(os.listdir(self.Output_PATH))>0:
                print("\033[1;31m[WARNING]:\033[0m Output_PATH文件夹非空, 本脚本可能会破坏文件夹结构或覆盖同名文件")
        else:
            os.makedirs(self.Output_PATH, exist_ok=True)

        self.Output_label_path = os.path.join(self.Output_PATH, "labels")
        self.Output_image_path = os.path.join(self.Output_PATH, "images")

        if len(self.Set_names)!=len(self.Set_ratios):
            raise SyntaxError("Sets_name与Set_ratio的长度必须一致且一一对应")
        for name in self.Set_names:
            label_path = os.path.join(self.Output_label_path, name)
            img_path = os.path.join(self.Output_image_path, name)
            if not os.path.exists(label_path):
                os.makedirs(label_path, exist_ok=True)
            if not os.path.exists(img_path):
                os.makedirs(img_path, exist_ok=True)
        if sum(self.Set_ratios)!=1:
            raise ValueError("Set_ratio所有切分比例之和必须为1")

        if self.Classes is str and self.Classes != "auto":
            if os.path.exists(self.Classes):
                self.Classes = detect_classes(self.Annotation_PATH, self.Classes)
            else:
                self.Classes = "auto"
        if self.Classes == "auto":
            self.Classes = detect_classes(self.Annotation_PATH)
        Output_classes_path = os.path.join(self.Output_PATH, "classes.txt")
        with open(Output_classes_path, "w", encoding="utf-8") as f:
            f.writelines([c+"\n" for c in self.Classes])

        if self.MODE not in ["copy", "cut"]:
            raise ValueError("MODE必须为 copy 或 cut")


kwargs = json.load(open("./Arguments.json", encoding="utf-8"))
P = Param(**kwargs)
