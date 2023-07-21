import pymysql as conn
db = conn.connect(host='localhost', user='root',
                  password='Omar@1234', port=3306, database='quiz_app')
cr = db.cursor()


def insert_user(t):
    sql = 'INSERT INTO user_info (fullname, email, mypassword) VALUES(%s, %s, %s)'
    cr.execute(sql, t)
    db.commit()


def login_user(p):
    sql = 'SELECT fullname=%s, mypassword%s FROM user_info'
    cr.execute(sql, p)
    db.commit()


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
