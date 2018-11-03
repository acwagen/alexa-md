import sqlite3

conn = sqlite3.connect('var/alexamd.db')

print("successful connection")

q = open('sql/data.sql', 'r').read()
print("successful query read")

c = conn.cursor()
c.executescript(q)
print("successful table population")

conn.commit()
c.close()
conn.close()
print("exiting")
