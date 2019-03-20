import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

#config
app.config["MONGO_DBNAME"] = 'cookBook'
app.config["MONGO_URI"] = 'mongodb+srv://lima:Chiquinho09@myfirstcluster-3jbxl.mongodb.net/cookBook?retryWrites=true'

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', recipes=mongo.db.recipes.find())
    
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)