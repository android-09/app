import random as r
from flask import *
from DBMS import *
app = Flask(__name__)
app.secret_key = "arfa"


@app.route('/')
def home():
    if (session.get("id")):
        return redirect("/userpage")

    else:
        return render_template('home.html')


@app.route('/adduser', methods=['POST'])
def adduser():
    # id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    passwd = request.form['password']
    t = (name, email, passwd)
    insert_user(t)

    return render_template('home.html', msg='register successfull')


@app.route('/login')
def login_info():
    return render_template('login.html')


@app.route("/updateform", methods=["POST"])
def updateform():
    if session["id"]:
        return render_template("updateform.html")
    else:
        return redirect("/login")


@app.route("/updateuser", methods=["POST"])
def updateuserview():
    name = request.form['name']
    email = request.form['email']
    passwd = request.form['password']
    id = session.get("id")
    t = (name, email, passwd, id)
    updateuserdb(t)
    session["uname"] = t[0]
    session["password"] = t[2]
    session["email"] = t[1]
    return redirect("/profile")


@app.route("/profile")
def userprofile():
    if session.get("id"):
        return render_template("profile.html")
    else:
        return redirect("/login")


@app.route("/admin")
def admin():
    if (session.get("isadmin")):
        return render_template("admin.html")
    else:
        return redirect("/")


@app.route("/logout")
def lgot():
    if (session.get("id")):
        session.clear()
        return redirect("/login")
    else:
        return redirect("/login")


@app.route("/userpage")
def userpage():
    if session.get("id"):
        return render_template("userPage.html")

    else:
        return render_template("home.html", msg="login is must")


@app.route('/playuser', methods=['POST'])
def play_user():
    name = request.form['name']
    passwd = request.form['password']
    # request.session['uid']
    p = (name, passwd)
    data = login_user(p)
    details = ()
    id = 0
    print(data)
    if data is not None:
        data = data[0]
        details = data[1:3]
        if p == details:
            session["id"] = data[0]
            session["uname"] = data[1]
            session["password"] = data[2]
            session["email"] = data[3]
            print(data[-1])
            if data[-1] == 0:
                session["isadmin"] = 0
                return redirect("/userpage")
            else:
                session["isadmin"] = 1
                return redirect("/admin")
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route('/ulist')
def usr_list():
    if (session["isadmin"]):
        ul = select_all()
        return render_template('userlist.html', ulist=ul)
    else:
        return redirect("/")


@app.route('/deluser', methods=['GET'])
def del_user():
    id = request.args.get('id')
    delete_user(id)
    return redirect('/ulist')


@app.route("/ubtuser")
def upduser():
    id = request.args.get("id")
    data = selectbyid(id)
    return render_template("updateregister.html", d=data)


@app.route("/updateuserdata", methods=["POST"])
def updateuserdata():
    user_id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    passwd = request.form['password']
    admin = 0
    if "uadmin" in request.form:
        admin = 1
    t = (name, email, passwd, admin, user_id)
    update_user(t)
    return render_template('admin.html')


@app.route("/play")
def play():
    if session.get("id"):
        operators = ("+", "-", "*", "//")
        question = str(r.randint(1, 9))+r.choice(operators) + \
            str(r.randint(1, 9))+r.choice(operators)+str(r.randint(1, 9))
        ans = eval(question)
        session["ans"] = ans
        print(question)
        print(ans)
        options = [ans, r.randint(1, 9), r.randint(1, 9), r.randint(1, 9)]
        r.shuffle(options)
        return render_template("play.html", q=question, op=options)
    else:
        return redirect("/")


@app.route("/submit")
def sub():
    if session.get("id"):
        return redirect("/play")


if __name__ == '__main__':
    app.run(debug=True, port=4000)
