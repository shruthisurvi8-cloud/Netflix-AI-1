import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_sql(question):

    prompt = f"""
You are an SQLite expert.

Table name: netflix

Columns:
show_id
type
title
director
cast
country
date_added
release_year
rating
duration
listed_in
description

Convert the user's question into ONLY a valid SQLite query.

Do not explain anything.
Return only SQL.

Question:
{question}
"""

    response = model.generate_content(prompt)

    sql = response.text.strip()

    # Remove markdown formatting
    sql = sql.replace("```sqlite", "")
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()