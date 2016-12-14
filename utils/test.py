import sqlite3

def sample_meme():
    f = "../data/dab.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute("SELECT owner, ref FROM memelist")
    hold = c.fetchall()

    db.commit()
    db.close()

    list = []
    for line in hold:
        print("Entry")
        print(line)
        dict = {}
        dict['creator'] = str(line[1])
        dict['create_ts'] = 'Monday, 12-Dec-16 12:39:25 UTC'
        dict['base64str'] = str(line[0])
        list.append(dict)

    return list

def get_username(userid):
    db1 = sqlite3.connect("../data/dab.db", check_same_thread=False)
    d1 = db1.cursor()
    q = 'SELECT username FROM userdata WHERE id='+str(userid)+';'
    d1.execute(q)
    r = d1.fetchall()
    db1.commit()
    db1.close()
    return r[0][0]

print(get_username(3))

def get_yours(user):
    db1 = sqlite3.connect("../data/dab.db", check_same_thread=False)
    d1 = db1.cursor()
    #q = 'SELECT memeid, price, ref FROM memelist WHERE username='+user+';'
    q = 'SELECT memeid, price, ref FROM memelist;'
    d1.execute(q)
    r = d1.fetchall()
    db1.commit()
    db1.close()
    ret = dict()
    for t in r:
        ret[t[2]] = [t[0], t[1]] #ref: [memeid, price]

    return ret


#print(get_yours("ss"))
#print(sample_meme())
