import sqlite3

conn = sqlite3.connect('var/alexamd.db')

print("successful connection")

q = open('sql/createTables.sql', 'r').read()
print("successful query read")

c = conn.cursor()
c.executescript(q)
print("successful query execution")

conn.commit()
c.close()
conn.close()
print("exiting")
