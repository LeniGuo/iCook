"""
Data preprocessing for RAG
"""
# reference:
# https://github.com/luisdrita/HyperFoods/tree/master/data/recipe1M%2B
# https://github.com/ritvikmath/nlp-recipe-project/tree/master/Data%20Cleaning

import json
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import pickle
import os

# 下载和加载必要的 NLTK 数据
nltk.download('stopwords')

# 定义文件路径
base_dir = 'src/rag/process_data/data/recipe1M+'
layer1_path = os.path.join(base_dir, 'layer1.json')

# 加载 Recipe1M+ 数据集
with open(layer1_path) as f:
    data = json.load(f)

# 解析和转换数据
ingredients = pd.json_normalize(data, record_path='ingredients', meta='id')
instructions = pd.json_normalize(data, record_path='instructions', meta='id')
recipes = pd.DataFrame(data)[["url", "title", "id"]]

# 将原料和步骤合并成单行
ingredient_single_line = ingredients.groupby("id")['text'].agg(lambda col: " || ".join(col)).reset_index(name="text")
instructions_single_line = instructions.groupby("id")['text'].agg(lambda col: " || ".join(col)).reset_index(name="text")

# 将合并后的数据与原食谱数据结合
joined = pd.merge(recipes, ingredient_single_line, on=['id'], how='left')
joined = pd.merge(joined, instructions_single_line, on=['id'], how='left')
joined = joined.rename(columns={'url': 'url', 'title': 'title', 'id': 'id', 'text_x': 'ingredients', 'text_y': 'instructions'})

# 合并标题、步骤和原料
joined["combined"] = joined["title"] + " --|||-- " + joined["instructions"] + " --|||-- " + joined["ingredients"]

# 字符串标准化
clean_words = {"c": "cup", "cups": "cup", "tablespoon": "tbsp", "tablespoons": "tbsp", "tbsps": "tbsp", "teaspoon": "tsp",
               "teaspoons": "tsp", "tsps": "tsp", "hours": "hour", "hr": "hour", "hrs": "hour", "minutes":"minute",
               "min":"minute", "mins":"minute", "pounds": "lb", "pound": "lb", "lbs": "lb", "one": "1", "two": "2",
               "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
               "ounce": "oz", "ounces": "oz", "ozs": "oz"}

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def normalize_string(s):
    s = re.sub(r"[(),.]", r"", s).lower().strip()
    words = s.split()
    words = [clean_words.get(w, ps.stem(w) if w not in stop_words else "") for w in words]
    return " ".join(words)

# 对数据进行标准化处理
joined["combined"] = joined["combined"].apply(normalize_string)

# 保存预处理后的数据
preprocessed_data_path = os.path.join(base_dir, 'preprocessed_recipe_data.pkl')
with open(preprocessed_data_path, 'wb') as f:
    pickle.dump(joined, f)

# 创建索引
index = {row['id']: row['combined'] for _, row in joined.iterrows()}

# 保存索引
recipe_index_path = os.path.join(base_dir, 'recipe_index.pkl')
with open(recipe_index_path, 'wb') as f:
    pickle.dump(index, f)

# 测试加载预处理数据和索引
with open(preprocessed_data_path, 'rb') as f:
    preprocessed_data = pickle.load(f)

with open(recipe_index_path, 'rb') as f:
    loaded_index = pickle.load(f)

# 输出测试结果
print(preprocessed_data.head())
print(list(loaded_index.items())[:5])
