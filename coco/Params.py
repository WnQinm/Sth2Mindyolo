import os
from dataclasses import dataclass, field
from .utils import detect_classes


@dataclass
class Param:
    Dataset_PATH: str = field(default="./cocodataset")
    Output_PATH: str = field(default="./yolodataset")

    Set_names: str = field(default_factory=lambda: ["train", "test"])

    MODE: str = field(default="copy")

    def __post_init__(self):
        self.anno_path = os.path.join(self.Dataset_PATH, "annotations")

        self.output_img_path = os.path.join(self.Output_PATH, "images")
        self.output_label_path = os.path.join(self.Output_PATH, "labels")
        for set_name in self.Set_names:
            os.makedirs(os.path.join(self.output_img_path, set_name), exist_ok=True)
            os.makedirs(os.path.join(self.output_label_path, set_name), exist_ok=True)

        self.Classes = detect_classes(self.anno_path)
        with open(os.path.join(self.Output_PATH, "classes.txt"), 'w', encoding='utf-8') as f:
            f.writelines([c+"\n" for c in self.Classes])
        self.Classes = {name:idx for idx, name in enumerate(self.Classes)}