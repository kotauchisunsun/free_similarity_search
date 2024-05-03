import fastapi
import os
from database import Database
import gradio as gr

DATABASE_PATH = os.getenv("DATABASE_PATH")

db = Database(DATABASE_PATH)
app = fastapi.FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

def search_doc(query: str, n: int):
    data = [
        {
            "question": record.page_content,
            "answer": record.metadata["answer"],
            "title": record.metadata["title"],
            "context": record.metadata["context"],
            "score": score
        }
        for record,score
        in db.query(query, n)
    ]
    return data

@app.get("/search")
def search(query:str, n:int=5):
    return search_doc(query,n)

with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("""
# 簡易あいまいFAQ検索

質問を入力すると、それに近い質問を検索します。[API Doc](/docs)

""")
    with gr.Blocks():
        question = gr.Textbox(label="質問", placeholder="質問を入力してください", value="坂本龍一の生誕地は？")
        n = gr.Number(label="検索数", value=5, interactive=True)
        answer = gr.Dataframe(headers=["score","question","answer","title","context"],datatype=["number","str","str","str","str"], type="array")
        button = gr.Button("検索")
        def format(query:str, n:int):
            return [
                [record["score"],record["question"], record["answer"], record["title"], record["context"]]
                for record
                in search_doc(query,int(n))
            ]
        button.click(format, inputs=[question,n], outputs=[answer])

app = gr.mount_gradio_app(app,demo,"/")