import os

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm, AddRecipeForm

#App config
app = Flask(__name__)
app.config['MONGO_URI']=os.environ.get("MONGO_URI")
app.config['SECRET_KEY']=os.environ.get("SECRET_KEY")

#wtfform secret key
app.secret_key = '123456789'

mongo = PyMongo(app)

#Collection
recipes_coll = mongo.db.recipes


#Home
@app.route('/')
@app.route('/index')
def index():
    # if 'username' in session:
    #     flash('You are already logged in as ' + session['username'])
    return render_template('index.html')
    
    
#All recipes 
@app.route('/recipes')
def recipes():
    recipes = recipes_coll.find()
    return render_template('recipes.html', page_title="Easy and Quick Recipes",  recipes=recipes)
    

#Each recipe view
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipes = recipes_coll.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', page_title="Easy and Quick Recipes" , recipes=recipes)
   

#Filter recipes
@app.route('/filter_recipes', methods = ['GET','POST'])
def filter_recipes():
    if request.method == 'POST':
        recipes = recipes_coll.find({ "$or": [ { "course": request.form["course"] }, { "cuisine": request.form["cuisine"] }, { "allergens": request.form["allergens"] }, { "author": request.form["author"] }] })
        print(recipes)
        # print(list(recipes))
        return render_template('recipes.html', recipes=recipes)
    return render_template('recipes.html', recipes=recipes)
    

# Add recipe view
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', recipes=recipes_coll.find())
    
# Insert recipe    
@app.route('/insert_recipe', methods = ['GET', 'POST'])
def insert_recipe(): 
    form = AddRecipeForm()
    recipes = recipes_coll
    if form.validate_on_submit():
        image = request.form['image']
        name =  request.form['name']
        author =  request.form['author']
        notes =  request.form['notes']
        course =  request.form['course']
        cuisine =  request.form['cuisine']
        allergens =  request.form.getlist('allergens')
        ingredient =  request.form.getlist('ingredient')
        step =  request.form.getlist('step')
        recipes.insert_one({'image': image, 'name': name, 'notes': notes, 'author': author, 'course': course, 'cuisine': cuisine, 'allergens': allergens,
            'ingredient': ingredient, 'step': step })
        return redirect(url_for('recipes'))  
    return render_template('addrecipe.html', page_title="Add your Own Recipe", form=form)
        

# Edit recipe
class AttributeDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    
@app.route('/edit_recipe/<recipes_id>', methods = ['GET', 'POST'])  
def edit_recipe(recipes_id):
    recipes = recipes_coll.find_one({"_id": ObjectId(recipes_id)})
    form = AddRecipeForm(obj=recipes)
    if form.validate_on_submit():
        recipes.image = form.image.data
        recipes.step = form.step.data
        recipes.allergens = form.allergens.data
        recipes.course = form.course.data
        recipes.ingredient = form.ingredient.data
        recipes.cuisine = form.cuisine.data
        recipes.author = form.author.data
        recipes.name = form.name.data
        recipes.notes = form.notes.data
        form.populate_obj(recipes)
        return redirect(url_for('recipes'))
    elif request.method == "GET":
        form.image.data = recipes['image']
        form.step.data = recipes['step']
        form.allergens.data = recipes['allergens']
        form.course.data = recipes['course']
        form.ingredient.data = recipes['ingredient']
        form.cuisine.data = recipes['cuisine']
        form.notes.data = recipes['notes']
        form.author.data = recipes['author']
        form.name.data = recipes['name']
        
    return render_template('editrecipe.html',recipes=recipes,page_title='Edit your Recipe', form=form)
    
    

# Update recipe
@app.route('/update_recipe/<recipes_id>', methods = ['GET','POST'])  
def update_recipe(recipes_id):
    recipes = recipes_coll
    recipes.update({"_id": ObjectId(recipes_id)},
    {
        'image':request.form.get('image'),
        'step':request.form.getlist('step'),
        'allergens':request.form.getlist('allergens'),
        'course':request.form.get('course'),
        'ingredient':request.form.getlist('ingredient'),
        'cuisine':request.form.get('cuisine'),
        'notes':request.form.get('notes'),
        'author':request.form.get('author'),
        'name':request.form.get('name')
        
    })
    
    return redirect(url_for('recipes'))
         
   

# Delete recipe
@app.route('/delete_recipe/<recipes_id>')
def delete_recipe(recipes_id):
    recipes = recipes_coll.remove({"_id": ObjectId(recipes_id)})
    flash('Recipe has been deleted', 'success')
    return redirect(url_for('recipes'))    

    
# User registration
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})
        
        if existing_user is None:
            users.insert({'name': request.form['username'], 'email': request.form['email'],'password': request.form['password'] })
            session['username'] = request.form['username']
            flash('Welcome {}, you are registered! You can login to your account now.'.format(form.username.data), 'success')
            return redirect(url_for('login'))
        flash('Username already exists!', 'danger')
    return render_template('register.html', page_title='New user Registration', form=form)
        
    
#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    #checking for data validation on Post
    if form.validate_on_submit():
        users = mongo.db.users
        login_user = users.find_one({'name':request.form['username'], 'email': request.form['email']})
        if login_user:
            if 'username' in session:
                flash('You are already logged in as ' + session['username'], 'success')
                return redirect(url_for('recipes'))
            if (request.form['password'] == login_user['password']):
                session['username'] = request.form['username']
                flash('Welcome {}, you are logged in!'.format(form.username.data), 'success')
                return redirect(url_for('recipes'))
            
        flash('Please check your details and try again', 'danger')
    
    return render_template('login.html', page_title='User Login', form=form)   
            
    
            
#User logout
@app.route('/logout')
def logout():
    #remove the user from the session
    session.pop('username', None)
    flash('You have been logout', 'success')
    return redirect(url_for('login'))

    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
