import sqlite3, dbm

db1 = sqlite3.connect("../data/dab.db")
d1 = db1.cursor()

def get_username(userid):
    d2 = db1.cursor()
    q = 'SELECT username FROM userdata WHERE id='+str(userid)+';'
    d2.execute(q)
    r = d2.fetchall()
    return r[0][0]

def your_meme(userid):
    d1.execute("SELECT owner, ref FROM memelist WHERE owner="+str(userid)+";")
    hold = d1.fetchall()
    list = []
    for line in hold:
        dict = {}
        dict['creator'] = str(get_username(line[1]))
        dict['create_ts'] = 'Monday, 12-Dec-16 12:39:25 UTC'
        dict['base64str'] = str(line[0])
        list.append(dict)

    return list

#print(your_meme(3))


def sample_memåe():
    c = db1.cursor()

    c.execute("SELECT owner, ref FROM memelist WHERE owner=3")
    hold = c.fetchall()

    list = []
    for line in hold:
        dict = {}
        dict['creator'] = str(get_username(line[0]))
        dict['create_ts'] = 'Monday, 12-Dec-16 12:39:25 UTC'
        dict['base64str'] = str(line[1])
        list.append(dict)

    return list

print(sample_meme())

db1.commit()
db1.close()
