from db import run_query

query = "SELECT * FROM netflix LIMIT 5"

result = run_query(query)

print(result)
