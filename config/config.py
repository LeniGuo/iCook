"""
/config 用于存放整个项目的配置参数信息
参考Baseline配置信息: https://github.com/SmartFlowAI/TheGodOfCookery/blob/main/config/config.py
"""


import os
from collections import defaultdict

Config = defaultdict(dict)

# rag
Config['rag_langchain'] = {
    'verbose': True,  # 是否打印详细的模型输入内容信息
    'dataset_config': {
        'file_path': "./data/XXX.json",
        'max_batch_size': 1000  # 条目数量上限
    },
    "HyDE": True,  # 是否使用HyDE
    # streamlit加载使用的相对路径格式和直接运行python文件使用的相对路径格式不同
    'faiss_config': {
        'save_path': './faiss_index',  # 保存faiss索引的路径
        'load_path': './rag_langchain/faiss_index',  # streamlit加载faiss索引的路径
        'search_type': "similarity_score_threshold",
        'search_kwargs': {"k": 3, "score_threshold": 0.6}
    },
    'bm25_config': {
        'dir_path': './retriever',  # 保存bm25检索器的文件夹的路径
        'save_path': './retriever/bm25retriever.pkl',  # 保存bm25检索器的路径
        'load_path': './rag_langchain/retriever/bm25retriever.pkl',  # streamlit加载bm25检索器的路径
        'search_kwargs': {"k": 3}
    },
    'bce_emb_config': {
        'model_name': os.environ.get('HOME') + "/models/bce-embedding-base_v1",
        'model_kwargs': {'device': 'cuda:0'},
        'encode_kwargs': {'batch_size': 32, 'normalize_embeddings': True, 'show_progress_bar': False}
    },
    'bce_reranker_config': {
        'model': os.environ.get('HOME') + "/models/bce-reranker-base_v1",
        'top_n': 1,
        'device': 'cuda:0',
        'use_fp16': True
    }
}