from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
app=Flask(__name__)

#users=[]
client=MongoClient('mongodb+srv://vu241fa04b38_db_users:blessy@cluster0.rnxvpf4.mongodb.net/?appName=Cluster0')
db=client["users-crt"]
user_collection=db["users"]
print("DB connected")

@app.route('/')
def home():
    return "Hello welcome to flask.db connected"

@app.route('/users',methods=["GET"])
def get_users():
    users=[]
    users_list=list(user_collection.find())
    for user in users_list:
        user["_id"]=str(user["_id"])
    return jsonify(users_list)

@app.route('/users',methods=["POST"])
def add_users():
    data=request.get_json()
    user={
       "name":data.get("name"),
       "email":data.get("email")
    }
    user_collection.insert_one(user)
    return jsonify({"message":"user inserted successfully"})

@app.route('/users/<id>',methods=['GET'])
def get_user_byID(id):
    user=user_collection.find_one(ObjectId(id))
    if user:
        user["_id"]=str(user["_id"])
        return jsonify(user)
    return jsonify({"message":"User not found"})

@app.route('/users/<id>',methods=['DELETE'])
def delete_user(id):
    user_collection.delete_one({"_id":ObjectId(id)})
    return jsonify({"message":"User deleted successfully"})
    #return jsonify({"message":"User not found"})
    
@app.route('/users/<id>',methods=['PUT'])
def update_user(id):
    data=request.get_json();
    updated_data={
        "name":data.get("name"),
        "email":data.get("email")
    }
    user_collection.update_one({"_id":ObjectId(id)},
    {"$set":updated_data})
    return jsonify({"message":"User updated successfully"})
    #return jsonify({"message":"User not found"})

@app.errorhandler(404)
def unavailable_page(error):
    return jsonify({"message":"Sorry this page is not available,please go away"})
    
if __name__ == "__main__":
    app.run(debug=True)