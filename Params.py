# -*- coding: utf-8 -*-
import os
from typing import Union, List
from dataclasses import dataclass
from utils import detect_classes


@dataclass
class Param:
    Annotation_PATH: str = "./Annotations"
    Image_PATH: str = "./JPEGImages"
    Output_PATH: str = "./output"

    Sets_name: List[str] = ["train", "val", "test"]
    Set_ratio: List[float] = [0.8, 0.1, 0.1]
    # TODO annotations里面有可能有classes.txt
    # list or str, eg: ["class1", "class2"] or "auto"
    Classes:Union[List[str], str]  = ["class1", "class2"]

    # ["copy", "cut"]
    MODE: str = "cut"

    # TODO 完善参数检查和后处理
    def __post_init__(self):
        self.Output_label_path = os.path.join(self.Output_PATH, "labels")
        self.Output_image_path = os.path.join(self.Output_PATH, "images")
        if self.Classes == "auto":
            self.Classes = detect_classes(self.Annotation_PATH)


# TODO 通过json文件加载参数
P = Param()