import sqlite3

db = sqlite3.connect("data/dab.db")
d = db.cursor()

# =========== START ACCESSOR METHODS =============
def get_meme(url):
    q = 'SELECT ref FROM memelist WHERE url=\"%s\";' % (url)
    d.execute(q)
    r = d.fetchall()

    return r

def get_owned(userid):
    q = 'SELECT memeid FROM memelist WHERE owner=%s' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r

def get_topfive():
    q = 'SELECT memeid FROM memelist ORDER BY price DESC LIMIT 5;'
    d.execute(q)
    r = d.fetchall()

    return r

# =========== END ACCESSOR METHODS =============

# =========== START GET METHODS ================
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
# =========== END GET METHODS ================

# =========== LOGIN/REGISTER =================
def auth(user, password):
    h = hashlib.sha1(password).hexdigest()

    if not user_available(user):
        q = 'SELECT * FROM userdata WHERE username=\"%s\";' % (user)
        d.execute(q)

        r = d.fetchall()

        #figure out how to parse r

        return True
    return False

def user_available(user):
    q = 'SELECT * FROM userdata WHERE username=\"%s\";' % (user)
    d.execute(q)

    r = d.fetchall()

    if (len(r) > 0):
        return False
    return True

def register(user, password):
    h = hashlib.sha1(password).hexdigest()

    if user_available(user):
        q = 'INSERT INTO userdata(username, password) VALUES (\"%s\", \"%s\");' % (user, password)
        d.execute(q)

        db.commit()
