# -*- coding: utf-8 -*-
import json
import argparse
from coco import coco2yolo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='./Arguments.json')
    args = parser.parse_args()

    kwargs = json.load(open(args.config, encoding="utf-8"))
    coco2yolo(**kwargs)