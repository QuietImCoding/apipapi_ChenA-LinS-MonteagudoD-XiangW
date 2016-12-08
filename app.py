import utils.auth,  hashlib, os, json, random
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
        return render_template('index.html')
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

@app.route("/make_meme")
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

        page = '''
<!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <script type="text/javascript" src="/static/js/jquery-3.1.1.min.js"></script>
    <script type="text/javascript" src="/static/js/tether.min.js"></script>
    <script type="text/javascript" src="/static/js/bootstrap.min.js"></script>

    <title>Meme Page</title>

</head>

<body>

    <!-- navbar -->
    <nav class="navbar navbar-fixed-top navbar-dark bg-inverse">
        <a class="navbar-brand text-success" href="#">The Meme Game</a>

        <ul class="nav navbar-nav nav-tabs bg-inverse">
            <li class="nav-item">
                    <form action="/home" class="btn btn-primary" style="background:transparent; border:none"><input type="submit" style="background:no\
ne; border:none" value="Home"/></form>
            </li>
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#">Meme Market</a>
                <div class="dropdown-menu bg-inverse text-danger">
                    <form action="/make_meme" class="btn btn-primary" style="background:transparent; border:none"><input type="submit" style="backgrou\
nd:none; border:none" value="Create a Meme"/></form>
                    <a class="dropdown-item text-muted" href="#">Buy a Meme</a>
                    <form action="/display_memes" class="btn btn-primary" style="background:transparent; border:none"><input type="submit" style="back\
ground:none; border:none" value="View My Memes"/></form>
                    <form action="/display_all_memes" class="btn btn-primary" style="background:transparent; border:none"><input type="submit" style="\
background:none; border:none" value="View All Memes"/></form>
                </div>
            </li>

<li>
            </li>
            <li class="nav-item">
              <form action="/logout" class="btn btn-primary" style="background:transparent; border:none"><input type="submit" style="background:none; \
border:none" value="Logout"/></form>

            </li>


            <span class="navbar-text lead float-xs-right text-muted">
                    Logged in as:
                <u>Marshall Mathers</u>
            </span>
</ul>
    </nav>
''' 
        
        #page += "<br><br><center><h5>%s</h5>" % (current_word)
        page += "<br><br><center>"
        for line in split_lines(example_used, len(example_used)/2):
            page += "<h5>%s</h5>" % (line)
        url_random = random.randrange(len(urls))
        page += "<img src='%s'/></center><br><br>" % urls[url_random]
        page += "</body></html>"
        return page

    return render_template('auth.html', action_type='login')
def getImages():
    global current_word, examples, definitions
    wordnik_key = "40dc55834c419934220050a79fd0655dbb1f88083bc729ad9"
    current_word = get_random_word(wordnik_key)
    examples = get_examples(wordnik_key, current_word)
    definitions = get_definition(wordnik_key, current_word)
    api_key = '8746e5a7e804588f2c14eee32778068b'
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



@app.route("/save_meme")
def save_meme():
    if(secret in session):
        #do the saving meme thing here
        #to save the meme and associate it with a user
        return render_template("gallery.html", action="user")
    return render_template('auth.html', action_type='login')

@app.route("/display_memes")
def display_memes():
    if(secret in session):
        #displays only user's memes
        return render_template("gallery.html", action="user")
    return render_template('auth.html', action_type='login')

@app.route("/display_all_memes")
def display_all_memes():
    if(secret in session):
        #this is to display all of the memes in the gallery
        return render_template("gallery.html", action="all")
    return render_template('auth.html', action_type='login')

@app.route("/home")
def return_home():
    if(secret in session):
        #this is to display all of the memes in the gallery
        return render_template("index.html")
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
        return redirect(url_for("index")) #redirect(url_for("log_em_in"))
    #else
    return render_template('auth.html', action_type='mk_act')

#======================================END__OF__ROUTAGE


if __name__ == "__main__":
    app.debug = True
    app.run() 
