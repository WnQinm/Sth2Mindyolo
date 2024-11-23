# VOC2MindYOLO

VOC数据集格式转换为[mindyolo](https://github.com/mindspore-lab/mindyolo)数据集格式

基于[Data_Trans](https://github.com/JieZzzoo/Data_Trans)修改，优化了代码泛用性，简化操作流程，只测试了基于mindyolo的目标检测相关项目场景

## 使用方法

修改`Arguments.json`中的各项参数，然后在终端`python main.py`即可

根据生成的`classes.txt`修改自己的yaml配置文件，然后通过`python train.py --config your_config.yaml`开始训练

- yaml配置文件参考[mindyolo configs](https://github.com/mindspore-lab/mindyolo/tree/master/configs)
- [train.py](https://github.com/mindspore-lab/mindyolo/blob/master/train.py)在mindyolo代码库下载
- checkpoint在[mindyolo 模型仓库](https://github.com/mindspore-lab/mindyolo/blob/master/docs/zh/modelzoo/benchmark.md)

## 参数说明

### Annotation_PATH

原VOC数据集的Annotations文件夹路径，其中存放所有xml格式的注释数据

### Image_PATH

原VOC数据集的JPEGImages文件夹路径，其中存放所有jpg格式的图片数据

### Output_PATH

脚本输出的yolo格式数据集路径

### Set_names

划分数据集名称

例如`[训练集, 验证集, 测试集]`

### Set_ratios

划分数据集所占比例，要与名称一一对应，所有比例总和必须为1

例如`[0.8, 0.1, 0.1]`，表示训练集占80%、验证集占10%，测试集占10%

### Classes

所有标签类别

允许三种输入：

1. 包含所有类别的列表，例如`[猫, 狗]`
2. 指定classes.txt路径，有些VOC格式训练集的Annotations文件夹下会存放classes.txt文件，包含所有的类别，可以将该文件路径作为此参数输入
3. “auto”，默认值，遍历Annotations文件夹下的所有xml文件，通过name标签统计所有类别

### MODE

图片拷贝模式，可选范围：`[copy, cut]`

- copy：默认值，不改动原来VOC数据集的内容，将图片复制一份到新数据集中
- cut：将原来VOC数据集中的图片直接移动到新数据集中

## 数据说明

使用了xml文件中的如下信息：

```xml
<annotation>
	<size>
		<width>xxx</width>
		<height>xxx</height>
	</size>
	<object>
		<name>xxx</name>
		<difficult>0</difficult>
		<bndbox>
			<xmin>xxx</xmin>
			<ymin>xxx</ymin>
			<xmax>xxx</xmax>
			<ymax>xxx</ymax>
		</bndbox>
	</object>
</annotation>
```

输出文件夹结构：

`````
${Output_PATH}
    - images
        - ${Set_names[0]}
            - xxx.jpg
        - ${Set_names[1]}
            - xxx.jpg
        ...
    - labels
        - ${Set_names[0]}
            - xxx.txt
        - ${Set_names[1]}
            - xxx.txt
        ...

    - ${Set_names[0]}.txt
    - ${Set_names[1]}.txt
    - ...
    - classes.txt
`````

