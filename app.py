import os
import uuid
import random as r
from flask import *
from DBMS import *

app = Flask(__name__)
app.secret_key = "arfa"


@app.route("/")
def home():
    if session.get("id"):
        return redirect("/quiztop")

    else:
        return render_template("home.html")


@app.route("/adduser", methods=["POST"])
def adduser():
    # id = request.form['id']
    name = request.form["name"]
    email = request.form["email"]
    passwd = request.form["password"]
    t = (name, email, passwd)
    insert_user(t)

    return render_template("home.html", msg="register successfull")


@app.route("/login")
def login_info():
    return render_template("login.html")


@app.route("/updateform", methods=["POST"])
def updateform():
    if session["id"]:
        return render_template("updateform.html")
    else:
        return redirect("/login")


@app.route("/updateuser", methods=["POST"])
def updateuserview():
    name = request.form["name"]
    email = request.form["email"]
    passwd = request.form["password"]
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
    if session.get("isadmin"):
        return render_template("admin.html")
    else:
        return redirect("/")


@app.route("/logout")
def lgot():
    if session.get("id"):
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


@app.route("/playuser", methods=["POST"])
def play_user():
    name = request.form["name"]
    passwd = request.form["password"]
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
                return redirect("/quiztop")
            else:
                session["isadmin"] = 1
                return redirect("/admin")
        else:
            return redirect("/login")
    else:
        return redirect("/login")


@app.route("/ulist")
def usr_list():
    if session["isadmin"]:
        ul = select_all()
        return render_template("userlist.html", ulist=ul)
    else:
        return redirect("/")


@app.route("/deluser", methods=["GET"])
def del_user():
    id = request.args.get("id")
    delete_user(id)
    return redirect("/ulist")


@app.route("/ubtuser")
def upduser():
    id = request.args.get("id")
    data = selectbyid(id)
    return render_template("updateregister.html", d=data)


@app.route("/updateuserdata", methods=["POST"])
def updateuserdata():
    user_id = request.form["id"]
    name = request.form["name"]
    email = request.form["email"]
    passwd = request.form["password"]
    admin = 0
    if "uadmin" in request.form:
        admin = 1
    t = (name, email, passwd, admin, user_id)
    update_user(t)
    return render_template("admin.html")


@app.route("/play")
def play():
    if session.get("id"):
        operators = ("+", "-", "*", "//")
        question = (
            str(r.randint(1, 9))
            + r.choice(operators)
            + str(r.randint(1, 9))
            + r.choice(operators)
            + str(r.randint(1, 9))
        )
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


### quiz top


@app.route("/quiztop")
def quiztop():
    user_id = session.get("id")
    # userの履歴を取得
    user_history = select_user_history(user_id)
    # すべてのクイズを取得
    quiz_all = select_quiz_all()
    return render_template("quiztop2.html", user_history=user_history, quiz_all=quiz_all)


### quiz detail


@app.route("/quiz", methods=["GET", "POST"])
def take_quiz():
    quiz_id = request.args.get("quiz_id")
    title = get_quiz_title(quiz_id)
    data = get_quiz_data(quiz_id)
    total_questions = len(data)

    if "current_quiz_index" not in session:
        session["current_quiz_index"] = 0

    if "score" not in session:
        session["score"] = 0

    current_quiz_index = session["current_quiz_index"]
    score = session["score"]

    if request.method == "POST":
        user_answer = request.form["user_answer"]
        correct_answer = data[current_quiz_index][3]

        print("user:", user_answer)
        print("answer:", correct_answer)

        if user_answer == correct_answer:
            session["score"] += 1
            print("correct")
        else:
            print("incorrect")

        session["current_quiz_index"] += 1
        current_quiz_index = session["current_quiz_index"]
        score = session["score"]

    if current_quiz_index >= total_questions:
        if total_questions > 0:
            result = int((score / total_questions) * 100)
        else:
            result = 0
        return render_template(
            "quizresult.html",
            title=title,
            quiz_id=quiz_id,
            score=score,
            result=result,
            total_questions=total_questions,
        )

    current_quiz = data[current_quiz_index]
    question = current_quiz[2]
    options = current_quiz[3:7]
    shuffled_options = list(options)
    r.shuffle(shuffled_options)

    print("--------------------")
    print("current_quiz_index:", current_quiz_index)
    print("session[current_quiz_index]:", session["current_quiz_index"])
    print("score:", score)
    print("--------------------")

    return render_template(
        "quizdetail.html",
        title=title,
        current_quiz=current_quiz,
        question_no=current_quiz_index + 1,
        question=question,
        options=shuffled_options,
        total_qns=total_questions,
    )


@app.route("/quiz/clear", methods=["GET"])
def clear_quiz_session():
    session.pop("current_quiz_index", None)
    session.pop("score", None)
    quiz_id = request.args.get("quiz_id")
    return redirect(url_for("take_quiz", quiz_id=quiz_id))


### quiz title admin


def save_file(file):
    UPLOAD_FOLDER = "static/images/title/"
    ext = os.path.splitext(file.filename)[1]
    filename = "images/title/" + str(uuid.uuid4()) + ext
    file_path = os.path.join(UPLOAD_FOLDER, filename.split("/")[-1])
    file.save(file_path)
    return filename


@app.route("/quiztitleadmin")
def quiztitleadmin():
    titles = select_quiz_all()
    return render_template("quiztitleadmin.html", titles=titles)


@app.route("/quiztitleadmin/add", methods=["POST"])
def quiztitleadmin_add():
    image_file = request.files.get("image_file")
    if image_file.filename != "":
        image_path = save_file(image_file)
    else:
        image_path = ""

    data = {
        "title": request.form["title"],
        "difficulty": request.form["difficulty"],
        "image": image_path,
    }
    add_title(data)
    return redirect("/quiztitleadmin")


@app.route("/quiztitleadmin/edit/<int:id>", methods=["POST"])
def quiztitleadmin_edit(id):
    data = {
        "ID": id,
        "title": request.form["title"],
        "difficulty": request.form["difficulty"],
    }

    image_file = request.files.get("image_file")
    if image_file and image_file.filename != "":
        old_image_path = request.form["old_image_path"]
        if old_image_path and os.path.exists(old_image_path):
            os.remove("/static/" + old_image_path)

        image_path = save_file(image_file)
        data["image"] = image_path
    else:
        data["image"] = request.form["old_image_path"]

    edit_title(data)
    return redirect("/quiztitleadmin")


@app.route("/quiztitleadmin/delete/<int:id>")
def quiztitleadmin_delete(id):
    delete_title(id)
    return redirect("/quiztitleadmin")


# クイズの問題をいれるところ
@app.route("/quizdetailadmin")
def quizdetailadmin():
    quiz_all = select_quiz_all()
    select_alldetail = get_alldetail()
    return render_template(
        "quizdetailadmin.html", quiz_all=quiz_all, select_alldetail=select_alldetail
    )


@app.route("/adddetailadmin", methods=["POST"])
def adddetailadmin():
    if request.method == "POST":
        quiz_id = request.form["quiz_id"]
        question = request.form["question"]
        selection1 = request.form["selection1"]
        selection2 = request.form["selection2"]
        selection3 = request.form["selection3"]
        selection4 = request.form["selection4"]
        comment = request.form["comment"]
        image = request.form["image"]
        q = (
            quiz_id,
            question,
            selection1,
            selection2,
            selection3,
            selection4,
            comment,
            image,
        )

        insert_detail(q)
        return redirect(url_for("quizdetailadmin"))
    # return render_template("quizdetailadmin.html")


@app.route("/updatedetail", methods=["POST"])
def updatedetail():
    if request.method == "POST":
        update_id = request.form["update_id"]
        update_quiz_id = request.form["update_quiz_id"]
        update_question = request.form["update_question"]
        update_selection1 = request.form["update_selection1"]
        update_selection2 = request.form["update_selection2"]
        update_selection3 = request.form["update_selection3"]
        update_selection4 = request.form["update_selection4"]
        update_comment = request.form["update_comment"]
        update_image = request.form["update_image"]
        u = (
            update_quiz_id,
            update_question,
            update_selection1,
            update_selection2,
            update_selection3,
            update_selection4,
            update_comment,
            update_image,
            update_id,
        )
        update_detail(u)
        return redirect("/quizdetailadmin")


@app.route("/deletedetail", methods=["POST"])
def deletedetail():
    if request.method == "POST":
        delete_id = request.form["delete_id"]
        d = (delete_id,)
        delete_detail(d)
        return redirect("/quizdetailadmin")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
