#!/bin/bash

# Change directory to /model
cd ./model

# Clone the repository
git clone https://www.modelscope.cn/zhanghuiATchina/zhangxiaobai_shishen2_full.git

rm zhangxiaobai_shishen2_full/pytorch_model.bin.index.json

curl -o "zhangxiaobai_shishen2_full/pytorch_model.bin.index.json" "https://www.modelscope.cn/api/v1/models/zhanghuiATchina/zhangxiaobai_shishen2_full/repo?Revision=master&FilePath=pytorch_model.bin.index.json"
