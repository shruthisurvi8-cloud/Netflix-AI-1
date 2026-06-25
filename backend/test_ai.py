from ai import generate_sql
from query_db import execute_query

question = "Show top 5 movies released after 2020"

sql = generate_sql(question)

print("Generated SQL:")
print(sql)

results = execute_query(sql)

print("\nResults:")
for row in results:
    print(row)