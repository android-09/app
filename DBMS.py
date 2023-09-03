import pymysql as conn
import os
#db = conn.connect(host='localhost', user='root',
#                  password='Omar@1234', port=3306, database='quiz_play')
db = conn.connect(host='127.0.0.1', user='root',
                  port=3306, database='quiz_play')
cr = db.cursor()


def insert_user(t):
    sql = 'INSERT INTO user_info (fullname, email, mypassword) VALUES(%s, %s, %s)'
    cr.execute(sql, t)
    db.commit()


def login_user(p):
    sql = 'SELECT id,fullname,mypassword,email,is_admin   FROM user_info where fullname=%s and mypassword=%s'
    cr.execute(sql, p)
    data = cr.fetchall()
    if data:
        return data
    else:
        return None


def select_all():
    sql = 'SELECT *FROM user_info'
    cr = db.cursor()
    cr.execute(sql)
    ul = cr.fetchall()
    db.commit()
    return ul


def delete_user(id):
    sql = 'DELETE FROM user_info WHERE ID=%s'
    cr = db.cursor()
    cr.execute(sql, id)
    db.commit()


def selectbyid(id):
    sql = 'SELECT * FROM user_info where ID=%s'
    cr = db.cursor()
    cr.execute(sql, id)
    ul = cr.fetchall()
    print(ul)
    db.commit()
    return ul[0]


def update_user(t):
    sql = 'update user_info set fullname=%s,email=%s,mypassword=%s,is_admin=%s where ID=%s'
    cr = db.cursor()
    cr.execute(sql, t)
    db.commit()


def updateuserdb(t):
    sql = 'update user_info set fullname=%s,email=%s,mypassword=%s where ID=%s'
    cr = db.cursor()
    cr.execute(sql, t)
    db.commit()


def insertrounds(t):
    sql = 'insert into gameplay (user_id,price) values(%s,%s)'
    cr = db.cursor()
    cr.execute(sql, t)
    db.commit()


def getamt(id):
    sql = 'select sum(price) from gameplay where user_id=%s'
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
    sql = 'SELECT * FROM quiz_title'
    cr = db.cursor()
    cr.execute(sql)
    db.commit()
    ul = cr.fetchall()
    return ul

# クイズのタイトル（個別）を取得
def select_quiz_title(quiz_id):
    sql = 'SELECT * FROM quiz_title WHERE ID=%s'
    cr = db.cursor()
    cr.execute(sql,quiz_id)
    db.commit()
    ul = cr.fetchall()
    return ul[0]

# クイズの詳細を取得
def select_quiz_detail(quiz_id):
    sql = 'SELECT * FROM quiz_detail WHERE quiz_id=%s'
    cr = db.cursor()
    cr.execute(sql,quiz_id)
    db.commit()
    ul = cr.fetchall()
    return ul

# userの履歴を取得
def select_user_history(user_id):
    sql = 'SELECT * FROM user_history WHERE user_id=%s'
    cr = db.cursor()
    cr.execute(sql,user_id)
    db.commit()
    ul = cr.fetchall()
    return ul



def add_title(data):
    with db.cursor() as cursor:
        sql = "INSERT INTO quiz_title (title, difficulty, image) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['title'], data['difficulty'], data['image']))
        db.commit()

def edit_title(data):
    with db.cursor() as cursor:
        sql = "UPDATE quiz_title SET title=%s, difficulty=%s, image=%s WHERE ID=%s"
        cursor.execute(sql, (data['title'], data['difficulty'], data['image'], data['ID']))
        db.commit()

def delete_title(id):
    with db.cursor() as cursor:
        sql = "SELECT image FROM quiz_title WHERE ID=%s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        if result:
            image_path = os.path.join('static', result[0])
            # 2. Delete the image from /static/images/title directory
            if os.path.exists(image_path):
                os.remove(image_path)

    # Now, delete the title from the database as it was done originally
    with db.cursor() as cursor:
        sql = "DELETE FROM quiz_title WHERE ID=%s"
        cursor.execute(sql, (id,))
        db.commit()