from flask import *
from DBMS import insert_user, login_user
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/adduser', methods=['POST'])
def adduser():
    # id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    passwd = request.form['password']
    t = (name, email, passwd)
    insert_user(t)
    return redirect('/')


@app.route('/login')
def login_info():
    return render_template('login.html')


@app.route('/playuser', methods=['POST'])
def play_user():
    name = request.form['name']
    passwd = request.form['password']
    p = (name, passwd)
    login_user(p)

    if p == login_user(p):
        pass
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
