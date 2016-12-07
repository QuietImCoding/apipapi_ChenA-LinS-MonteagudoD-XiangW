import utils.auth,  hashlib, os
from flask import Flask, render_template, session, request, redirect, url_for

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
