import os

from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm, AddRecipeForm

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
    

#Each recipe view
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipes = recipes_coll.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', page_title="Easy and Quick Recipes" , recipes=recipes)
   

# Filter recipes
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
@app.route('/edit_recipe/<recipes_id>', methods= ['GET', 'POST'])
def edit_recipe(recipes_id):
    form = AddRecipeForm()
    recipes_to_edit = recipes_coll.find_one({"_id": ObjectId(recipes_id)})
    all_recipes = recipes_coll.find()
    return render_template('editrecipe.html', page_title="Edit your Recipe", cookBook=recipes_to_edit, recipes=all_recipes, form=form)
    
    



    






#User registration
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form =  RegisterForm()
    #checking for data validation on Post
    if form.validate_on_submit():
         flash('Hi {}, your account has been created!'.format({form.username.data}), 'success')
         return redirect(url_for('index'))
    return render_template('register.html', page_title="New User Register", form=form)  
    
    

#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
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