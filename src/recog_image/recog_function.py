"""
Provide functions for interface to use
Functions related to prediction and saving.
"""

import sys
import argparse
import os
import yaml
import shutil

current_dir = os.getcwd()
path = os.path.join(current_dir, 'ultralytics')
sys.path.append(path)  # Path 以Autodl为例
print(path)

from ultralytics import YOLO

def copy_and_rename_predict_folder():
    current_dir = os.getcwd()

    # 检查 'latest_runs/predict' 文件夹是否存在
    predict_dir = os.path.join(current_dir, 'ultralytics', 'latest_runs', 'predict')
    if not os.path.exists(predict_dir):
        print(f"'{predict_dir}' does not exist.")
        return

    # 生成 'runs' 文件夹路径
    runs_dir = os.path.join(current_dir, 'runs')
    os.makedirs(runs_dir, exist_ok=True)

    # 获取所有现有的 runs 目录，找到最大后缀号
    runs_dirs = [d for d in os.listdir(runs_dir) if d.startswith('predict')]
    max_suffix = 0
    for dir_name in runs_dirs:
        try:
            suffix = int(dir_name.replace('predict', ''))
            if suffix > max_suffix:
                max_suffix = suffix
        except ValueError:
            continue

    # 生成新的后缀号
    new_suffix = max_suffix + 1
    new_folder_name = f'predict{new_suffix}'
    new_folder_path = os.path.join(runs_dir, new_folder_name)

    # 复制并重命名目录
    shutil.copytree(predict_dir, new_folder_path)
    # 删除原始目录
    shutil.rmtree(predict_dir)

def main(opt, image_path):
    yaml = opt.cfg
    model = YOLO(yaml)
    model.info()
    model = YOLO('ultralytics/runs/detect/train11/weights/best.pt')
    model.predict(image_path, save_dir = 'ultralytics/latest_runs/predict' , save=True, show_labels=True)
    copy_and_rename_predict_folder()
    #save_dir = './runs/results'
    # 自己设置路径


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default= r'ultralytics/yolov8n.pt', help='initial weights path')
    parser.add_argument('--artifact_alias', type=str, default='latest', help='W&B: Version of dataset artifact to use')

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


def obtain_label_path(image_path):
    # 得到数字形式label的存放的路径
    current_dir = os.getcwd()  # 获取当前工作目录的绝对路径
    # 找到最新的predict文件
    predict_folder_path = os.path.join(current_dir, 'runs')
    predict_files = [f for f in os.listdir(predict_folder_path) if f.startswith('predict')]
    latest_predict_file = max(predict_files, key=lambda x: int(x.lstrip('predict')))
    # label.txt的路径
    image_name=extract_name_from_path(image_path)+'.txt'

    label_num_path = os.path.join(current_dir, 'runs', latest_predict_file, 'labels', image_name)
    #这里仅获取最新的predict，即就是数字最大的predict文件，因此，若是要清理predict文件，必须从后往前清理，否则会出错。

    return label_num_path

def extract_name_from_path(file_path):
    # 获取最后一个 '/' 之后的部分
    file_name_with_extension = file_path.rsplit('/', 1)[-1]
    # 获取最后一个 '.' 之前的部分
    file_name = file_name_with_extension.split('.', 1)[0]
    return file_name

def convert_labels(file_path):
    # 读取取数字label，并将其转为名字label
    # 定义数字标签到物品名的映射关系
    label_map = {
        0: 'Bitter melon', 1: 'Brinjal', 2: 'Cabbage', 3: 'Calabash', 4: 'Capsicum',
        5: 'Cauliflower', 6: 'Cherry', 7: 'Garlic', 8: 'Ginger', 9: 'Green Chili',
        10: 'Kiwi', 11: 'Lady finger', 12: 'Onion', 13: 'Potato', 14: 'Sponge Gourd',
        15: 'Tomato', 16: 'apple', 17: 'avocado', 18: 'banana', 19: 'cucumber',
        20: 'dragon fruit', 21: 'egg', 22: 'guava', 23: 'mango', 24: 'orange',
        25: 'oren', 26: 'peach', 27: 'pear', 28: 'pineapple', 29: 'strawberry',
        30: 'sugar apple', 31: 'watermelon', 32: 'chicken', 33: 'pork', 34: 'beef'
    }

    # 读取文件内容并转换标签
    labels = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            label = int(parts[0])
            if label in label_map:
                labels.append(label_map[label])

    # 返回识别到的标签
    return labels


def get_filename(path): # 输入存放文件夹的路径
    # 生成新的文件名,返回存储label的路径

    i = 1
    while True:
        file_name = f"label{i}.txt"
        file_path = os.path.join(path, file_name)
        if not os.path.exists(file_path):
            return file_path
        i += 1

def save_label(food_labels, label_save_path):
    content = '\n'.join(food_labels)  # 使其txt每行输出一个label
    # 确保目录存在
    os.makedirs(os.path.dirname(label_save_path), exist_ok=True)

    # 将内容写入文件
    with open(label_save_path, 'w') as file:
        file.write(content)
    return
