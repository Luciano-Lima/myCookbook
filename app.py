import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm

#App config
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

#wtfform secret key
app.secret_key = '123456789'

mongo = PyMongo(app)

#Collection
recipes_coll = mongo.db.recipes

# home
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    

#All recipes 
@app.route('/recipes')
def recipes():
    recipes = recipes_coll.find()
    return render_template('recipes.html', page_title="Easy and Quick Recipes",  recipes=recipes)
    
    
#Add recipes 
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html')    
    

#User registration
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form =  registerForm()
    #checking for data validation on Post
    if form.validate_on_submit():
         flash('Hi {}, your account has been created!'.format({form.username.data}), 'success')
         return redirect(url_for('index'))
    return render_template('register.html', page_title="New User Register", form=form)  
    
    
#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    #checking for data validation on Post
    if form.validate_on_submit():
        flash('Your are logged in', 'success')
        return redirect(url_for('index'))
    else:
        flash('Please check your details and try again', 'danger')
    return render_template('login.html', page_title='User Login', form=form)        


    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)