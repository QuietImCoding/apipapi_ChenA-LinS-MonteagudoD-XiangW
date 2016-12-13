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
    print("Hold")
    print(hold)
    for line in hold:
        print("Entry")
        print(line)
        dict = {}
        dict['creator'] = str(line[1])
        dict['create_ts'] = 'Monday, 12-Dec-16 12:39:25 UTC'
        dict['base64str'] = line[0]
        list.append(dict)

    return list

print(sample_meme())
