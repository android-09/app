import pymysql as conn
import os

# db = conn.connect(host='localhost', user='root',
#                  password='Omar@1234', port=3306, database='quiz_play')

db = conn.connect(host="127.0.0.1", user="root", port=3306, database="quiz_play")

cr = db.cursor()


def insert_user(t):
    sql = "INSERT INTO user_info (fullname, email, mypassword) VALUES(%s, %s, %s)"
    cr.execute(sql, t)
    db.commit()


def login_user(p):
    sql = "SELECT id,fullname,mypassword,email,is_admin   FROM user_info where fullname=%s and mypassword=%s"
    cr.execute(sql, p)
    data = cr.fetchall()
    if data:
        return data
    else:
        return None


def select_all():
    sql = "SELECT *FROM user_info"
    cr = db.cursor()
    cr.execute(sql)
    ul = cr.fetchall()
    db.commit()
    return ul


def delete_user(id):
    sql = "DELETE FROM user_info WHERE ID=%s"
    cr = db.cursor()
    cr.execute(sql, id)
    db.commit()


def selectbyid(id):
    sql = "SELECT * FROM user_info where ID=%s"
    cr = db.cursor()
    cr.execute(sql, id)
    ul = cr.fetchall()
    print(ul)
    db.commit()
    return ul[0]


def update_user(t):
    sql = "update user_info set fullname=%s,email=%s,mypassword=%s,is_admin=%s where ID=%s"
    cr = db.cursor()
    cr.execute(sql, t)
    db.commit()


def updateuserdb(t):
    sql = "update user_info set fullname=%s,email=%s,mypassword=%s where ID=%s"
    cr = db.cursor()
    cr.execute(sql, t)
    db.commit()


def insertrounds(t):
    sql = "insert into gameplay (user_id,price) values(%s,%s)"
    cr = db.cursor()
    cr.execute(sql, t)
    db.commit()


def getamt(id):
    sql = "select sum(price) from gameplay where user_id=%s"
    cr = db.cursor()
    cr.execute(sql, id)
    db.commit()
    price = cr.fetchall()
    sql = "delete from gameplay where user_id=%s"
    cr = db.cursor()
    cr.execute(sql, id)
    db.commit()
    print(price)
    if price[0][0]:
        return int(price[0][0])
    else:
        return 0


# すべてのクイズを取得
def select_quiz_all():
    sql = "SELECT * FROM quiz_title"
    cr = db.cursor()
    cr.execute(sql)
    db.commit()
    ul = cr.fetchall()
    return ul


# クイズのタイトル（個別）を取得
def get_quiz_title(quiz_id):
    sql = "SELECT * FROM quiz_title WHERE ID=%s"
    cr = db.cursor()
    cr.execute(sql, quiz_id)
    ul = cr.fetchall()
    return ul[0][1]


# クイズの詳細を取得
def get_quiz_data(quiz_id):
    sql = "SELECT * FROM quiz_detail WHERE quiz_id=%s"
    cr = db.cursor()
    cr.execute(sql, (quiz_id,))
    ul = cr.fetchall()
    return ul


# userの履歴を取得
def select_user_history(user_id):
    sql = "SELECT * FROM user_history INNER JOIN quiz_title ON user_history.quiz_category = quiz_title.ID WHERE user_id=%s"
    # sql = "SELECT * FROM user_history LEFT JOIN quiz_title ON user_history.quiz_category = quiz_title.title WHERE user_id=%s"
    # sql = "SELECT * FROM user_history WHERE user_id=%s"
    cr = db.cursor()
    cr.execute(sql, user_id)
    db.commit()
    ul = cr.fetchall()
    return ul


def add_title(data):
    with db.cursor() as cursor:
        sql = "INSERT INTO quiz_title (title, difficulty, image) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data["title"], data["difficulty"], data["image"]))
        db.commit()


def edit_title(data):
    with db.cursor() as cursor:
        sql = "UPDATE quiz_title SET title=%s, difficulty=%s, image=%s WHERE ID=%s"
        cursor.execute(
            sql, (data["title"], data["difficulty"], data["image"], data["ID"])
        )
        db.commit()


def delete_title(id):
    with db.cursor() as cursor:
        sql = "SELECT image FROM quiz_title WHERE ID=%s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()

        image_path = None
        if result and result[0]:
            image_path = os.path.join("static", result[0])

        if image_path and os.path.isfile(image_path):
            os.remove(image_path)

    with db.cursor() as cursor:
        sql = "DELETE FROM quiz_title WHERE ID=%s"
        cursor.execute(sql, (id,))
        db.commit()


# クイズの追加
def insert_detail(q):
    sql = "INSERT INTO quiz_detail (quiz_id, question, selection1, selection2, selection3, selection4, comment, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    cr.execute(sql, q)
    db.commit()


# クイズ詳細を取得
def get_alldetail():
    sql = "SELECT * FROM quiz_detail"
    cr = db.cursor()
    cr.execute(sql)
    db.commit()
    ul = cr.fetchall()
    return ul


# クイズアップデート
def update_detail(u):
    sql = "UPDATE quiz_detail SET quiz_id=%s,question=%s,selection1=%s,selection2=%s,selection3=%s,selection4=%s,comment=%s,image=%s where id=%s"
    cr.execute(sql, u)
    db.commit()

# クイズを削除
def delete_detail(d):
    sql = "DELETE FROM quiz_detail where id=%s"
    cr.execute(sql, d)
    db.commit()