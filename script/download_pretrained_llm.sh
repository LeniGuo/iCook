#!/bin/bash

# Install git-lfs: https://zhuanlan.zhihu.com/p/146683392
apt install git-lfs
apt update
git lfs install

# Change directory to /model
cd model
mkdir zhanghuiATchina
cd zhanghuiATchina

# Clone the repository
git clone https://www.modelscope.cn/zhanghuiATchina/zhangxiaobai_shishen2_full.git