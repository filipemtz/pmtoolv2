
import sqlite3
import json

with open("config.json", "r") as f:
    db_name = json.load(f)["db"]

# Initialize connection to the database
con = sqlite3.connect(db_name)
cur = con.cursor()

# set the responsible for the tasks
result = cur.execute("UPDATE scrum_task SET responsible_id='1'")
con.commit()

# Listar todos os produtos
print("tasks:")
result = cur.execute("SELECT * FROM scrum_task")
for row in result:
    print(row)

con.close()
