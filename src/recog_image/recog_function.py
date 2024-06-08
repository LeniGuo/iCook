"""
Provide functions for interface to use
Functions related to prediction and saving.
"""

import sys
import argparse
import os
import shutil

# 设置工作目录为脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
print(f"Recognition working directory: {os.getcwd()}")

# 添加ultralytics路径
ultralytics_path = os.path.join(current_dir, 'ultralytics')
sys.path.append(ultralytics_path)

from ultralytics import YOLO

def main(opt, image_path):
    yaml = opt.cfg
    model = YOLO(yaml)
    model.info()
    model = YOLO(os.path.join(current_dir, 'ultralytics', 'weights', 'best.pt'))
    # Path = os.path.join(current_dir, 'ultralytics', 'latest_runs', 'predict')
    # 可选的路径，存在bug，已废用
    model.predict(image_path, save=True, show_labels=True, save_txt=True, conf=0.3)

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default=os.path.join(current_dir, 'ultralytics', 'yolov8n.pt'), help='initial weights path')
    parser.add_argument('--artifact_alias', type=str, default='latest', help='W&B: Version of dataset artifact to use')

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


def obtain_label_path(image_path):
    current_dir = os.getcwd()  # 获取当前工作目录的绝对路径
    # 找到最新的predict文件
    predict_folder_path = os.path.join(current_dir, 'runs', 'detect')

    # 获取所有的 predict 文件夹，包括没有后缀的
    predict_files = [f for f in os.listdir(predict_folder_path) if f.startswith('predict')]

    # 检查是否只有一个 predict 文件夹
    if len(predict_files) == 1 and predict_files[0] == 'predict':
        latest_predict_file = 'predict'
    else:
        latest_predict_file = max(predict_files, key=lambda x: int(x.lstrip('predict') or '0'))

    image_name = extract_name_from_path(image_path) + '.txt'
    label_num_path = os.path.join(predict_folder_path, latest_predict_file, 'labels', image_name)
    return label_num_path


def extract_name_from_path(file_path):
    file_name_with_extension = os.path.basename(file_path)  # 获取文件名和扩展名
    file_name = os.path.splitext(file_name_with_extension)[0]  # 去掉扩展名
    return file_name

def convert_labels(file_path):
    label_map = {
        0: 'Bitter melon', 1: 'Brinjal', 2: 'Cabbage', 3: 'Calabash', 4: 'Capsicum',
        5: 'Cauliflower', 6: 'Cherry', 7: 'Garlic', 8: 'Ginger', 9: 'Green Chili',
        10: 'Kiwi', 11: 'Lady finger', 12: 'Onion', 13: 'Potato', 14: 'Sponge Gourd',
        15: 'Tomato', 16: 'apple', 17: 'avocado', 18: 'banana', 19: 'cucumber',
        20: 'dragon fruit', 21: 'egg', 22: 'guava', 23: 'mango', 24: 'orange',
        25: 'oren', 26: 'peach', 27: 'pear', 28: 'pineapple', 29: 'strawberry',
        30: 'sugar apple', 31: 'watermelon', 32: 'chicken', 33: 'pork', 34: 'beef'
    }

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print("No ingredients detected")
        return None

    # 若存在，即检测到了食材
    labels = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            label = int(parts[0])
            if label in label_map:
                labels.append(label_map[label])

    return labels

def get_filename(path):  # 输入存放文件夹的路径
    i = 1
    while True:
        file_name = f"label{i}.txt"
        file_path = os.path.join(path, file_name)
        if not os.path.exists(file_path):
            return file_path
        i += 1

def save_label(food_labels, label_save_path):
    if food_labels is None:
        content = 'None'
    else:
        content = '\n'.join(food_labels)  # 使其txt每行输出一个label

    # 确保目录存在
    os.makedirs(os.path.dirname(label_save_path), exist_ok=True)

    # 将内容写入文件
    with open(label_save_path, 'w') as file:
        file.write(content)
    return

