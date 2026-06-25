import pandas as pd
import sqlite3

# Read CSV file
df = pd.read_csv("data/netflix_titles.csv")

# Create SQLite database
conn = sqlite3.connect("database/netflix.db")

# Create table and insert data
df.to_sql("netflix", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")