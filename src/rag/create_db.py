import json
import os
import pickle
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
import sys
from config import load_config


def load_dataset(file_path, max_batch_size):
    print("开始加载数据集")
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    if max_batch_size > 0:
        json_data = json_data[:max_batch_size]
    print("数据集加载完成")
    return json_data

def build_split_docs(json_data, emb_strategy):
    print("开始构建待编码文档集")
    split_docs = []
    for i in range(len(json_data)):
        question = json_data[i]['conversation'][0]['input']
        if "做" not in question:
            question += "的做法"
        answer = json_data[i]['conversation'][0]['output']
        if emb_strategy['source_caipu']:
            split_docs.append(Document(page_content=question + "\n" + answer))
        if emb_strategy['HyQE']:
            split_docs.append(Document(page_content=question, metadata={"caipu": question + "\n" + answer}))
    print("待编码文档集构建完成")
    return split_docs

def load_embeddings(bce_emb_config):
    print("开始加载编码模型")
    bce_emb_config["encode_kwargs"]["show_progress_bar"] = True
    embeddings = HuggingFaceEmbeddings(**bce_emb_config)
    print("编码模型加载完成")
    return embeddings

def build_bm25_retriever(split_docs, bm25_config):
    print("开始构建BM25检索器")
    bm25retriever = BM25Retriever.from_documents(documents=split_docs)
    bm25retriever.k = bm25_config['search_kwargs']['k']

    if not os.path.exists(bm25_config['dir_path']):
        os.mkdir(bm25_config['dir_path'])
    pickle.dump(bm25retriever, open(bm25_config['save_path'], 'wb'))
    print("BM25检索器构建完成")
    return bm25retriever

def build_vector_database(split_docs, embeddings, rag_model_type):
    print("开始编码向量数据库")
    if rag_model_type == "chroma":
        vectordb = Chroma.from_documents(documents=split_docs, embedding=embeddings,
                                         persist_directory=load_config('rag_langchain', 'chroma_config')['save_path'])
        vectordb.persist()
    else:
        faiss_index = FAISS.from_documents(documents=split_docs, embedding=embeddings,
                                           distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE)
        faiss_index.save_local(load_config('rag_langchain', 'faiss_config')['save_path'])
    print("向量数据库编码完成")

def main():
    sys.path.append('..')

    dataset_config = load_config('rag', 'dataset_config')
    file_path = dataset_config['file_path']
    max_batch_size = dataset_config['max_batch_size']
    json_data = load_dataset(file_path, max_batch_size)

    hyde = load_config('rag', 'HyDE')
    split_docs = build_split_docs(json_data, hyde)

    bce_emb_config = load_config('rag', 'bce_emb_config')
    embeddings = load_embeddings(bce_emb_config)

    bm25_config = load_config('rag', 'bm25_config')
    bm25retriever = build_bm25_retriever(split_docs, bm25_config)

    rag_model_type = load_config('rag', 'rag_model_type')
    build_vector_database(split_docs, embeddings, rag_model_type)

if __name__ == "__main__":
    main()
