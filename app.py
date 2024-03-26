from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive =request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup =BeautifulSoup(data.text,'html.parser')
    og_img= soup.select_one('meta[property="og:image"]')
    og_title=soup.select_one('meta[property="og:title"]')
    og_des =soup.select_one('meta[name="description"]')
    img = og_img['content']
    title = og_title['content']
    des = og_des['content']
    doc = {
        'image' : img,
        'title' : title,
        'description' : des,
        'star' :star_receive,
        'comment' : comment_receive,
    }
    db.moviesV2.insert_one(doc)
    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    move_list = list(db.moviesV2.find({},{'_id':False}))
    return jsonify({'movies':move_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)