import sqlite3
import os

conn = sqlite3.connect("../data.db")
c = conn.cursor()

c.execute("INSERT INTO services (name, port) VALUES (?, ?)", ('test_service', 1234))
c.execute("INSERT INTO exploits (filename, service_id) VALUES (?, ?)", ('exploit.sh', 1))
conn.commit()