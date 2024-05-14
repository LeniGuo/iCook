"""
/recog_image is for Image Recognition.
interface.py integrates all the external interfaces of this module.
"""

import os
import recog_function
import sys

current_dir = os.getcwd()
path = os.path.join(current_dir, 'ultralytics')
sys.path.append(path)


def recog_image(image_path, save_path='../../public/label'):  # 输入图片的路径，以及结果保存的路径
    # 检测图片

    opt = recog_function.parse_opt()
    recog_function.main(opt, image_path) # 用YOLOv8模型识别

    label_num_path = recog_function.obtain_label_path(image_path)
    food_labels = recog_function.convert_labels(label_num_path)  # 这是检测到食材的列表形式
    label_save_path = recog_function.get_filename(save_path)
    recog_function.save_label(food_labels, label_save_path)  # 保存结果
    print('Recognition result:', food_labels)
    print('Recognition result already saved to: ', label_save_path)
    return food_labels


if __name__ == "__main__":
    image_path = 'test.jpg'  # 输入要识别的图片路径

    label_save_path = '../../public/label'
    recog_image(image_path)
