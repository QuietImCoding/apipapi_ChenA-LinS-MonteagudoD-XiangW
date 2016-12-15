import sqlite3

db = sqlite3.connect("dab.db", check_same_thread=False)
d = db.cursor()

q = '''
SELECT * FROM memelist;
'''

print d.execute(q).fetchall()