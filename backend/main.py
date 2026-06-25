from fastapi import FastAPI
from ai import generate_sql
from query_db import execute_query

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Netflix AI API Running"}


@app.get("/ask")
def ask(question: str):

    sql = generate_sql(question)

    results = execute_query(sql)

    return {
        "question": question,
        "sql": sql,
        "results": results
    }