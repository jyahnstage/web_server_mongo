from flask import Flask, render_template, request
from data import Articles
from models import MyMongo
from config import MONGODB_URL

app = Flask(__name__)

mymongo = MyMongo(MONGODB_URL, 'os')

@app.route('/', methods=['GET', 'POST'])
def index():
    data = Articles()
    return render_template('index.html' , data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            mymongo.user_insert(username, email, phone, password)
            return "success"

    # elif request.method == "GET":
    #             return render_template('register.html', data=0)


            # db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)s

            # sql = f'SELECT * FROM user WHERE email = %s'
            # curs.execute(sql, email)

            # rows = curs.fetchall()  
            # print(rows)
            # if rows:
            #     return render_template('register.html', data=1)
            # else:
            #     result = mysql.insert_user(username, email, phone, password)
            #     print(result)
            #     return redirect('/login')
            
        
        # elif request.method == "GET":
        #     return render_template('register.html', data=0)

if __name__ =="__main__":
    app.run(debug=True , port=9999)