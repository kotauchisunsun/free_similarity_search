import fire
from database import Database
import csv
from tqdm import tqdm
import json

class Command:
    def create(self, model_path:str, model_name = "ja_core_news_lg", collection_name = "default"):
        Database.create(model_path=model_path, model_name=model_name, collection_name=collection_name)
        
    def dump_csv(self, json_path:str, csv_path:str):
        with open(csv_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["question","answer","title","context"],quoting=csv.QUOTE_ALL)
            writer.writeheader()

            with open(json_path) as f:
                data = json.load(f)
                for record in data["data"]:
                    question = record["paragraphs"][0]["qas"][0]["question"]
                    answer = record["paragraphs"][0]["qas"][0]["answers"][0]["text"]
                    title = record["title"]
                    context = record["paragraphs"][0]["context"]

                    csv_record = {
                        "question": question,
                        "answer": answer,
                        "title": title,
                        "context": context
                    }

                    writer.writerow(csv_record)

    def add_csv(self, model_path:str, csv_path:str):
        db = Database(model_path)
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for record in tqdm(reader):
                db.add(
                    question=record["question"],
                    metadata={
                        k:v
                        for k,v 
                        in record.items()
                        if k != "question"
                    }                
                )

    def query(self, model_path:str, question:str):
        db = Database(model_path)
        return db.query(question)
    
if __name__=="__main__":
    fire.Fire(Command)