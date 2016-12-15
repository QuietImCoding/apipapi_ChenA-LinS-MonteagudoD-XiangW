import utils.auth,  hashlib, os, json, random, utils.dbm
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
import urllib, math, sys
from itertools import count, groupby

app = Flask(__name__)

app.secret_key = os.urandom(32)
secret = 'secret_cookie_key'

#========================================ROUTAGE

#either shows user their home (stories edited by them), or redirect to login
@app.route("/")
def index():
    if (secret in session):
        name = session[secret]
        money = utils.dbm.get_balance(session[secret])
        memelist = utils.dbm.get_topfive()
        yourmemes = utils.dbm.get_your_topfive(utils.dbm.get_id(session[secret]))
        return render_template('index.html', moneys = money, memeList = memelist, yourMemes = yourmemes)
    return render_template('auth.html', action_type='login')

#The login, this here processes ur entered info, ships it on
@app.route("/login", methods=["POST"])
def log_em_in():
    given_user = request.form["username"]
    given_pass = request.form["password"]

    hashPassObj = hashlib.sha1()
    hashPassObj.update(given_pass)
    hashed_pass = hashPassObj.hexdigest()

    are_u_in = utils.auth.login(given_user, hashed_pass)

    if(are_u_in == True):
        session[secret]=given_user
        return redirect(url_for('index'))
    #else:
    #return redirect(url_for("log_em_in"))
    return render_template('auth.html', action_type='login')
    #return redirect(url_for("log_em_in"))

#Logs out, pops session    
@app.route("/logout")
def log_em_out():
    print session
    session.pop(secret)
    return redirect(url_for("index")) #redirect(url_for("log_em_in"))

@app.route("/make_meme", methods=["GET","POST"])
def make_a_meme():
    if(secret in session):
        global current_word, examples, definitions
        response = getImages()
        photos = []
        for photo in response['photos']['photo']:
            photos.append([photo['farm'], photo['server'], photo['id'], photo['secret']])
        urls = []
        for photo in photos:
            urls.append("https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (photo[0], photo[1], photo[2], photo[3]))
        example_random = random.randrange(len(examples))
        example_used = examples[example_random]
        money = utils.dbm.get_balance(session[secret])
        print(urls[0])
        return render_template('meme.html', action_type='make', image_url=urls[0], moneys = money )

    return render_template('auth.html', action_type='login')

@app.route("/buy_meme", methods=["GET", "POST"])
def disp_buymeme():
    if request.method=="GET":
        return redirect(url_for("index"))
#    buyerid = utils.dbm.get_id(request.form[secret])
    buyerid = utils.dbm.get_id(session[secret])
    sellerid = utils.dbm.get_owner(request.form['memeid'])
    memeid = request.form['memeid']
    price = utils.dbm.get_price(memeid)
    if (buyerid != sellerid):
        utils.dbm.exchange_meme(sellerid, buyerid, price, memeid)

    return redirect(url_for("index"))

def getImages():
    global current_word, examples, definitions
    keyfile = open("wordnik.key", 'r')
    wordnik_key = keyfile.read()
    keyfile.close();
    current_word = get_random_word(wordnik_key)
    examples = get_examples(wordnik_key, current_word)
    definitions = get_definition(wordnik_key, current_word)
    keyfile = open("flickr.key", 'r')
    api_key = keyfile.read()
    keyfile.close();
    response = urllib.urlopen('https://api.flickr.com/services/rest/?' + urllib.urlencode({'api_key':api_key, 'safe_search':'1', 'method':'flickr.photos.search', 'tags':current_word, 'format':'json', 'nojsoncallback':'1'}))
    response_data = json.loads(response.read())
    response_value = response_data['photos']['total']
    if response_value==0:
        return getImages()
    else:
        return response_data
def get_examples(api_key, word):
    resp = urllib.urlopen('http://api.wordnik.com/v4/word.json/' + word + '/examples?' + urllib.urlencode({'api_key': api_key}))
    examples_data = json.loads(resp.read())
    examples = [item['text'] for item in examples_data['examples']]
    return examples
def get_definition(api_key, word):
    resp = urllib.urlopen('http://api.wordnik.com/v4/word.json/' + word + '/definitions?' + urllib.urlencode({'api_key': api_key}))
    definitions_data = json.loads(resp.read())
    definitions = [item['text'] for item in definitions_data]
    return definitions
def get_random_word(api_key):
    resp = urllib.urlopen(
        'http://api.wordnik.com/v4/words.json/randomWord?' +
        urllib.urlencode({'minCorpusCount': 10000, 'api_key': api_key}))
    random_word_data = json.loads(resp.read())
    return random_word_data['word']
def split_lines(s, step):
    words = s.split()
    firsthalf = ""
    secondhalf = ""
    upper = 0
    for i in range(int(math.ceil(len(words)/2.0))):
        firsthalf += words[upper] + " "
        upper += 1
    for i in range(int(math.floor(len(words)/2.0))):
        secondhalf += words[upper] + " "
        upper += 1
    splits = [firsthalf, secondhalf]
    return splits

    c = count()
    chunks = sentence.split()
    return [' '.join(g) for k, g in groupby(chunks, lambda i: c.next() // step)]

@app.route("/save_meme", methods=["GET", "POST"])
def save_meme():
    if(secret in session):
        #do the saving meme thing here
        #to save the meme and associate it with a user
        utils.dbm.add_meme(utils.dbm.get_id(session[secret]),request.form['meme']) 
        #return render_template("gallery.html", action="user")

        return redirect(url_for("display_my_memes"))
    return render_template('auth.html', action_type='login')

@app.route("/display_my_memes")
def display_my_memes():
    if(secret in session):
        #displays only user's memes
        memelist = utils.dbm.get_yours(utils.dbm.get_id(session[secret]))
        money = utils.dbm.get_balance(session[secret])
        return render_template("gallery.html", action="user", sampleMemes = memelist, moneys = money)
    return render_template('auth.html', action_type='login')

@app.route("/display_all_memes")
def display_all_memes():
    if(secret in session):
        #this is to display all of the memes in the gallery
        print(utils.dbm.get_id(str(session[secret])))
        memelist = utils.dbm.sample_meme()
        money = utils.dbm.get_balance(session[secret])
        return render_template("gallery.html", action="all", sampleMemes = memelist, moneys = money)
    return render_template('auth.html', action_type='login')

@app.route("/home")
def return_home():
    if(secret in session):
        #this is to display all of the memes in the gallery
        return redirect(url_for("index"))
    return render_template('auth.html', action_type='login')


@app.route("/make_account")
def make_dat_account():
    return render_template('auth.html', action_type="mk_act")

#to make account
@app.route("/create_account", methods = ['POST'])
def create_dat_account():
    wanted_user = request.form["username"]
    email = request.form["email"]
    wanted_pass1 = request.form["password1"]
    wanted_pass2 = request.form["password2"]

    hashPassObj1 = hashlib.sha1()
    hashPassObj1.update(wanted_pass1)
    hashed_pass1 = hashPassObj1.hexdigest()

    hashPassObj2 = hashlib.sha1()
    hashPassObj2.update(wanted_pass2)
    hashed_pass2 = hashPassObj2.hexdigest()

    is_user_now = utils.auth.make_account(wanted_user, hashed_pass1, hashed_pass2, email)

    if(is_user_now == True):
        #return redirect(url_for("log_em_in"))
        session[secret] = wanted_user
        return redirect(url_for("index")) #redirect(url_for("log_em_in"))
    #else
    return render_template('auth.html', action_type='mk_act')

#======================================END__OF__ROUTAGE


if __name__ == "__main__":
    app.debug = True
    app.run() 
