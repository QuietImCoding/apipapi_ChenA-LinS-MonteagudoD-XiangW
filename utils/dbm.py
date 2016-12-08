import sqlite3

db = sqlite3.connect("../data/dab.db")
d = db.cursor()

# =========== START ACCESSOR METHODS =============

# takes dataurl of image, returns price of meme 
def get_price(url):
    q = 'SELECT price FROM memelist WHERE ref=\"%s\";' % (url)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes dataurl of image, returns owner of meme
def get_owner(url):
    q = 'SELECT owner FROM memelist WHERE ref=\"%s\";' % (url)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes session username, returns numerical id of username in db
def get_id(username):
    q = 'SELECT id FROM userdata WHERE username=\"%s\";' % (username)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes dataurl of image, returns amt of times meme was sold
def get_amtsold(url):
    q = 'SELECT amtsold FROM memelist WHERE ref=\"%s\";' % (url)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

# takes numerical userid, returns list of memes owned by user
def get_owned(userid):
    q = 'SELECT memeid FROM memelist WHERE owner=%s;' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0]

# returns dataurl of all memes
def get_all():
    q = 'SELECT ref FROM memelist'
    d.execute(q)
    r = d.fetchall()

    return r[0]

# returns dataurls of the five most expensive memes
def get_topfive():
    q = 'SELECT ref FROM memelist ORDER BY price DESC LIMIT 5;'
    d.execute(q)
    r = d.fetchall()

    return r[0]

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
def add_meme(price, owner, url):
    q = 'INSERT INTO memelist(price, owner, amtsold, ref) VALUES (%s, %s, 1, \"%s\");' % (price, owner, url)
    d.execute(q)

    db.commit()

def set_owner(url, nowner):
    q = 'UPDATE memelist SET owner=%s WHERE url=\"%s\";' % (nowner, url)
    d.execute(q)
    db.commit()

def set_price(url, nprice):
    q = 'UPDATE memelist SET price=%s WHERE url=\"%s\";' % (nprice, url)
    d.execute(q)

    db.commit()

def incrmt_amtsold(url):
    q = 'UPDATE memelist SET amtsold=amtsold + 1 WHERE url=\"%s\";' % (url)
    d.execute(q)

    db.commit()

def set_balance(userid, nbalance):
    q = 'UPDATE userdata SET balance=%s WHERE username=\"%s\";' % (nbalance, userid)
    d.execute(q)

    db.commit()

def set_lastmemesold(userid, nmemeid):
    q = 'UPDATE userdata SET lastmemesold=%s WHERE username=\"%s\";' % (nmemeid, userid)
    d.execute(q)

    db.commit()

# =========== END MUTATOR METHODS ================
