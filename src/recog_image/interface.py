"""
/recog_image is for Image Recognition.
interface.py integrates all the external interfaces of this module.
# 注意，只能通过终端运行，使用python src/recog_image/interface.py运行
"""

'''
三大肉类，以及水果的识别能力尚可，识别蔬菜的能力有限
'''

import os
import recog_function
import sys

# 设置工作目录为脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 添加ultralytics路径
ultralytics_path = os.path.join(current_dir, 'ultralytics')
sys.path.append(ultralytics_path)


def recog_image(image_path, save_path=None):  # 输入图片的路径，以及结果保存的路径
    if save_path is None:
        save_path = os.path.abspath(os.path.join(current_dir, '../../public/label'))

    # 检测图片
    opt = recog_function.parse_opt()
    recog_function.main(opt, image_path)  # 用YOLOv8模型识别

    label_num_path = recog_function.obtain_label_path(image_path)
    food_labels = recog_function.convert_labels(label_num_path)  # 这是检测到食材的列表形式
    label_save_path = recog_function.get_filename(save_path)
    recog_function.save_label(food_labels, label_save_path)  # 保存结果
    print('Recognition result:', food_labels)
    print('Recognition result already saved to: ', label_save_path)
    return food_labels


if __name__ == "__main__":

    # 注意，只能通过终端运行，使用python src/recog_image/interface.py运行

    image_path = os.path.abspath(os.path.join(current_dir, 'img_input_test', 'beef.png'))  # 输入要识别的图片路径, 绝对路径

    label_save_path = os.path.abspath(os.path.join(current_dir, '../../public/label'))
    recog_image(image_path, label_save_path)
