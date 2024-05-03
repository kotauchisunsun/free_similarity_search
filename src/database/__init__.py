import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
import configparser
import os

class Database:
    def __init__(self, model_path: str):
        config = configparser.ConfigParser()
        config.read(Database.get_config_path(model_path))

        model_name = config["DEFAULT"]["model_name"]
        collection_name = config["DEFAULT"]["collection_name"]

        embedding_function = SpacyEmbeddings(model_name=model_name)

        persistent_client = chromadb.PersistentClient(model_path)
        self.db = Chroma(client=persistent_client,collection_name=collection_name,embedding_function=embedding_function)

    @staticmethod
    def create(model_path:str, model_name = "ja_core_news_md", collection_name = "default"):
        persistent_client = chromadb.PersistentClient(path=model_path)
        embedding_function = SpacyEmbeddings(model_name=model_name)
        persistent_client.create_collection(name=collection_name,embedding_function=embedding_function)

        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "collection_name": collection_name,
            "model_name": model_name
        }
        with open(Database.get_config_path(model_path), "w") as configfile:
            config.write(configfile)

    def add(self, question: str, metadata):
        self.db.add_texts(texts=[question],metadatas=[metadata])

    def query(self, question:str, n=10):
        return self.db.similarity_search_with_score(question,k=n)        

    @classmethod
    def get_config_path(cls,model_path: str):
        return os.path.join(model_path,"config.ini")