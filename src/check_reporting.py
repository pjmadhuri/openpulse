import sqlite3

DB_PATH = "data/openpulse.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

print("\nREPORTING TABLE COLUMNS")
print("========================")

cursor.execute("""
    PRAGMA table_info(repo_health_summary)
""")

columns = cursor.fetchall()

for column in columns:
    print(column[1])

print("\nREPORTING DATA")
print("========================")

cursor.execute("""
    SELECT *
    FROM repo_health_summary
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()