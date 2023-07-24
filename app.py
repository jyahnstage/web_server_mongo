from flask import Flask, render_template, request, redirect, session
import pyautogui
from data import Articles
from models import MyMongo
from config import MONGODB_URL
from pymongo import *
import pprint
from functools import wraps

app = Flask(__name__)
app.secret_key = "My_Key"

mymongo = MyMongo(MONGODB_URL, 'os')

def is_logged(f):
       @wraps(f)
       def logged(*args, **kwargs):
            if 'is_logged' in session:
                return f(*args, **kwargs)
            else:
                return redirect('/login')
       return logged

def is_admin(f):
      @wraps(f)
      def admin(*args, **kwargs):
            if session['username'] == 'admin':
                  return f(*args, **kwargs)
            else:
                  return redirect('/login')
      return admin

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
@is_logged
@is_admin
def admin():
      return render_template('admin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')

            lookup = mymongo.find_user(email)
            if lookup:
                   return redirect ('/register')
                   
            else:
                   if username == "admin":
                        return redirect('/register')
                   else:     
                        mymongo.user_insert(username, email, phone, password)
                        return redirect('/login')           
    
    elif request.method == "GET":
                return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if  request.method == "GET":
                return render_template('login.html')
    
    elif request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            result = mymongo.verify_password(password, email)
            if result == 3:
                return render_template('register.html', message="none")
            elif result == 2:
                   return render_template('login.html', message="wrong")
            elif result == 1:
                   user = mymongo.find_user(email)
                   session['is_logged'] = True
                   session['username'] = user['username']
                   return render_template('index.html', message=user)
            
@app.route('/list')
def list():
    data = mymongo.find_data()
    # for i in data:
    #        print(i)
    return render_template('list.html', data = data)

@app.route('/create_at', methods=['GET', 'POST'])
@is_logged
def create():
    if  request.method == "POST":
            title = request.form.get('title')
            desc = request.form.get('desc')
            author = request.form.get('author')
            result = mymongo.insert_data(title, desc, author)
            print(result)
            return "입력 성공"
    elif  request.method == "GET":
           return render_template('create_at.html')
    
@app.route('/logout')
def logout():
       session.clear()
       return redirect ('/login')

if __name__ =="__main__":
    app.run(debug=True , port=9999)