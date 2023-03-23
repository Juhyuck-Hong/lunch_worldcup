from flask import Flask, render_template, request, jsonify
import random
from pymongo import MongoClient
from pprint import pprint
import json

with open('mongoDB_auth.json', 'r') as j:
    auth = json.load(j)

id = list(auth.keys())[0]
pw = auth[id]

client = MongoClient(f'mongodb+srv://{id}:{pw}@juhyukhong.q0dawlr.mongodb.net/?retryWrites=true&w=majority')
db = client.lunch_worldcup

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/results", methods=["POST"])
def result_post():
    user_name = request.form["user_name"]
    chosen_name = request.form["chosen_name"]
    doc = {'name': user_name,
           'result': chosen_name}
    db.results.insert_one(doc)
    return jsonify({'msg': '점심메뉴 월드컵 완료!'})

@app.route("/results", methods=["GET"])
def result_get():
    all_list = list(db.results.find({}, {'_id':False}))
    return jsonify({'results': all_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)