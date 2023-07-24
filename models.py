from pymongo import MongoClient
import datetime
import pprint
from passlib.hash import pbkdf2_sha256 
import pymysql
from bson.objectid import ObjectId
from config import MONGODB_URL

def hash_password(original_password):
    salt = 'eungok'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

def check_password(input_password, hashed_password):
    salt = 'eungok'
    password = input_password + salt
    result = pbkdf2_sha256.verify(password, hashed_password)    
    return result


class MyMongo:
    def __init__(self, db_url, database):
        self.database = database
        self.client = MongoClient(db_url)
        
    def user_insert(self, username, email, phone, password):
        db = self.client.os
        users = db.users
        pw = hash_password(password)
        user = {"username": username,
                "email": email,
                "phone": phone,
                "password": pw,
                "create_at": datetime.datetime.now()
                }
        result = users.insert_one(user)
        print(result)
        return "success"

    def verify_password(self, input_password, email):
        db = self.client.os
        users = db.users
        user = users.find_one({'email':email})
        if user:
            result = check_password(input_password, user['password'])
            if result:
                print("인증 성공")
                return 1
            else:
                print("인증 실패")
                return 2
        else:
            print("회원정보가 없습니다.")
            return 3
        
    def find_user(self, email):
        db = self.client.os
        users = db.users
        user = users.find_one({'email': email})
        print(user)
        return user 

    def find_data(self):
        db = self.client.os
        lists = db.lists
        list = lists.find()
        # for i in list:
        #     print (i)
        return list

    def insert_data(self, title, desc, author):
        db = self.client.os
        lists = db.lists
        list = {"title": title,
                "desc": desc,
                "author": author,
                "create_at": datetime.datetime.now()
                }
        result = lists.insert_one(list)
        print(result)
        return "success"


# mymongo = MyMongo(MONGODB_URL, 'os')
# mymongo.find_user("6@naver.com")
# # mymongo.user_insert("KIM", "2@naver.com","010-1111-1111", '1234')
# mymongo.verify_password("1234", ObjectId('64ba2ab2935cc47e04bd5bf8'))



# mongodb_URI = MONGODB_URL
# client = MongoClient(mongodb_URI)
# # print(client.list_database_names())

# db = client.os
# users = db.users
# # print(client.list_database_names())

# hashpass = hash_password("1234")

# user = {"username": "Jane",
#         "email": "1@naver.com",
#         "phone": "010-9999-9999",
#         "password": hashpass,
#         "create_at": datetime.datetime.utcnow()
#         }
# result = users.insert_one(user)
# print(result)
# print(user)
# post_id = collection.insert_one(post).inserted_id
# print(post_id)
# print(db.list_collection_names())
# pprint.pprint(collection.find_one())

# user = users.find_one({'_id': ObjectId('64ba2ab2935cc47e04bd5bf8')})
# print(user['password'])

# check_password('1234', '$pbkdf2-sha256$29000$JWQMgTAG4Fwrxdib8773vg$HShTNZlOc0qI6WFOmbUzS/ncTAFGG6pB.j4Omb2tWPI' )
# check_password('1234', user['password'])

