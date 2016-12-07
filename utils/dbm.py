import sqlite3
import hashlib

mdb = sqlite3.connect("data/dab.db")
memes = mdb.cursor()

def get_meme(url):
    q = 'SELECT ref FROM memelist WHERE url=\"%s\";' % (url)
    memes.execute(q)
    r = memes.fetchall()

    return r

def get_owned(userid):
    q = 'SELECT memeid FROM memelist WHERE owner=%s' % (userid)
    memes.execute(q)
    r = memes.fetchall()

    return r

def get_topfive():
    q = 'SELECT memeid FROM memelist ORDER BY price DESC LIMIT 5;'
    memes.execute(q)
    r = memes.fetchall()

    return r

def add_meme(price, owner, url):
    q = 'INSERT INTO memelist(price, owner, amtsold, ref) VALUES (%s, %s, 1, \"%s\");' % (price, owner, url)
    memes.execute(q)

    mdb.commit()

def set_owner(url, nowner):
    q = 'UPDATE memelist SET owner=%s WHERE url=\"%s\";' % (nowner, url)
    memes.execute(q)

    mdb.commit()

def set_price(url, nprice):
    q = 'UPDATE memelist SET price=%s WHERE url=\"%s\";' % (nprice, url)
    memes.execute(q)

    mdb.commit()

def incrmt_amtsold(url):
    q = 'UPDATE memelist SET amtsold=amtsold + 1 WHERE url=\"%s\";' % (url)
