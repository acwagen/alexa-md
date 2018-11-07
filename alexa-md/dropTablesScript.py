import sqlite3
import os

project_root = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(os.path.join(project_root, 'var', 'alexamd.db'))

print("successful connection")

q = open(os.path.join(project_root, 'sql', 'dropTables.sql'), 'r').read()
print("successful query read")

c = conn.cursor()
c.executescript(q)
print("successful dropTables")

conn.commit()
c.close()
conn.close()
print("exiting")
