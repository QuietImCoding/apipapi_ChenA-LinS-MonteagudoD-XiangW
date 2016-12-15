import sqlite3

db = sqlite3.connect("data/dab.db", check_same_thread=False)
d = db.cursor()

# =========== START ACCESSOR METHODS =============

# takes memeid, returns price of meme 
def get_price(memeid):
    q = 'SELECT price FROM memelist WHERE memeid=\"%s\";' % (memeid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes memeid, returns owner of meme
def get_owner(memeid):
    q = 'SELECT owner FROM memelist WHERE memeid=\"%s\";' % (memeid)
    d.execute(q)
    r = d.fetchall()

    print r
    return r[0][0]

# takes userid, returns username
def get_username(userid):
    q = 'SELECT username FROM userdata WHERE id='+str(userid)+';'
    d.execute(q)
    r = d.fetchall()
    
    return r[0][0]

# takes session username, returns numerical id of username in db
def get_id(username):
    q = 'SELECT id FROM userdata WHERE username=\"%s\";' % (username)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes memeid, returns amt of times meme was sold
def get_amtsold(memeid):
    q = 'SELECT amtsold FROM memelist WHERE memeid=\"%s\";' % (memeid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes numerical userid, returns list of memes owned by user
def get_owned(userid):
    q = 'SELECT memeid FROM memelist WHERE owner=%s;' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0]

# returns dataurl, price, and memeid of all memes
def get_all():
    q = 'SELECT memeid, price, ref FROM memelist;'
    d.execute(q)
    r = d.fetchall()

    ret = dict()
    for t in r:
        ret[t[2]] = [t[0], t[1]] #ref: [memeid, price]

    return ret

#returns dataurl, price, and memeid of user's memes
def get_yours(userid):
    d.execute("SELECT memeid, ref, price FROM memelist WHERE owner="+str(userid)+";")
    hold = d.fetchall()

    list = []
    for line in hold:
        dict = {}
        dict['creator'] = str(get_username(userid))
        dict['create_ts'] = 'Monday, 12-Dec-16 12:39:25 UTC'
        dict['base64str'] = str(line[1])
        dict['memeid'] = str(line[0])
        dict['memeprice'] = str(line[2])
        list.append(dict)

    return list


def sample_meme():
    f = "data/dab.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute("SELECT owner, ref, memeid, price FROM memelist")
    hold = c.fetchall()

    db.commit()
    db.close()

    list = []
    for line in hold:
        dict = {}
        dict['creator'] = str(get_username(line[0]))
        dict['create_ts'] = 'Monday, 12-Dec-16 12:39:25 UTC'
        dict['base64str'] = str(line[1])
        dict['memeid'] = str(line[2])
        dict['memeprice'] = str(line[3])
        list.append(dict)

    return list

# returns dataurls of the five most expensive memes
def get_topfive():
    q = 'SELECT ref, price  FROM memelist ORDER BY price DESC LIMIT 5;'
    d.execute(q)
    r = d.fetchall()

    list = []
    for line in r:
        dict = {}
        dict['base64str'] = str(line[0])
        dict['memeprice'] = str(line[1])
        list.append(dict)
        
    return list

def get_your_topfive(userid):
    q = 'SELECT ref, price  FROM memelist WHERE owner='+str(userid)+' ORDER BY price DESC LIMIT 5;'
    d.execute(q)
    r = d.fetchall()

    list = []
    for line in r:
        dict = {}
        dict['base64str'] = str(line[0])
        dict['memeprice'] = str(line[1])
        list.append(dict)
        
    return list

# takes a numerical userid, returns (int)balance of user
def get_balance(userid):
    q = 'SELECT balance FROM userdata WHERE username=\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes a numerical userid, returns numerical memeid of last meme sold by user
def get_lastmemesold(userid):
    q = 'SELECT lastmemesold FROM userdata WHERE username=\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes a numerical userid, returns a list of user info
def get_info(userid):
    q = 'SELECT username, nickname, dob, email, location, balance, lastmemesold FROM userdata WHERE id=%s' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0]

# takes a numerical memeid, returns dataurl of the image
def get_ref(memeid):
    q = 'SELECT ref FROM memelist WHERE memeid=%s;' % (memeid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# =========== END ACCESSOR METHODS =============

# =========== START MUTATOR METHODS ================

# takes price/numerical ownerid/dataurl, saves to memelist
def add_meme(ownerid, url):
    q = 'INSERT INTO memelist(price, owner, amtsold, ref) VALUES (100, %s, 1, \"%s\");' % (ownerid, url)
    print q
    d.execute(q)

    db.commit()

# takes dataurl/numerical ownerid, sets current ownerid to nownerid
def set_owner(url, nownerid):
    q = 'UPDATE memelist SET owner=%s WHERE url=\"%s\";' % (nownerid, url)
    d.execute(q)
    db.commit()

# takes dataurl/price, sets current price to nprice
def set_price(url, nprice):
    q = 'UPDATE memelist SET price=%s WHERE url=\"%s\";' % (nprice, url)
    d.execute(q)

    db.commit()

# takes memeid, increments amtsold by one
def inc_amtsold(memeid):
    q = 'UPDATE memelist SET amtsold=amtsold + 1 WHERE memeid=\"%s\";' % (memeid)
    d.execute(q)

    db.commit()

# takes numerical userid/balance, sets current balance to nbalance
def set_balance(userid, nbalance):
    q = 'UPDATE userdata SET balance=%s WHERE username=\"%s\";' % (nbalance, userid)
    d.execute(q)

    db.commit()

# takes numerical userid/memeid, sets user's lastmemesold to nmemeid
def set_lastmemesold(userid, nmemeid):
    q = 'UPDATE userdata SET lastmemesold=%s WHERE username=\"%s\";' % (nmemeid, userid)
    d.execute(q)

    db.commit()

# buyer buys meme (memeid) from seller, incrmentamtsold 
def exchange_meme(seller, buyer, price, memeid):
    
    q = 'UPDATE userdata SET balance=balance+'+str(price)+' WHERE id='+str(seller)+';'
    d.execute(q)
    q = 'UPDATE userdata SET balance=balance-'+str(price)+' WHERE id='+str(buyer)+';'
    d.execute(q)
    q = 'UPDATE memelist SET owner=%s WHERE memeid=%s;' % (buyer, memeid)
    d.execute(q)
    q = 'UPDATE memelist SET price = price + 10 WHERE memeid=%s;' % (memeid)
    d.execute(q)

    inc_amtsold(memeid)

    db.commit()
# =========== END MUTATOR METHODS ================

