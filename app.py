import os

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm, AddRecipeForm
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_bcrypt import Bcrypt


#App config
app = Flask(__name__)
app.config['MONGO_URI']=os.environ.get("MONGO_URI")
app.config['SECRET_KEY']=os.environ.get("SECRET_KEY")

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


mongo = PyMongo(app)
# intialising bcrypt
bcrypt = Bcrypt(app)

#Collection
recipes_coll = mongo.db.recipes

login_manager = LoginManager()
login_manager.init_app(app)


# User section manager  
@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_id = users.find_one({'_id': ObjectId(user_id)})
    return User(user_id)


#Home
@app.route('/')
@app.route('/index')
def index():
    recipes = recipes_coll.find()
    return render_template('index.html', recipes=recipes)
    
    
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
        print(request.form)
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
    print(request.form)
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
        form.step.data = ''.join(recipes['step'])
        form.allergens.data = recipes['allergens']
        form.course.data = recipes['course']
        form.ingredient.data = ''.join(recipes['ingredient'])
        form.cuisine.data = recipes['cuisine']
        form.notes.data = recipes['notes']
        form.author.data = recipes['author']
        form.name.data = recipes['name']
        
    return render_template('editrecipe.html',recipes=recipes,page_title='Edit your Recipe', form=form)
        
    


# Update recipe
@app.route('/update_recipe/<recipes_id>', methods = ['GET','POST'])  
def update_recipe(recipes_id):
    recipes = recipes_coll
    print(request.form)
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
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User = mongo.db.users
        user = User.find_one({'username': request.form['username']})
        if user is None:
            User.insert({'username': request.form['username'], 'email': request.form['email'],'password': pw_hash })
            session['username'] = request.form['username']
            flash('Welcome {}, you are registered! You can login to your account now.'.format(form.username.data), 'success')
            return redirect(url_for('login'))
        flash('Username already exists!', 'danger')
    return render_template('register.html', page_title='New user Registration', form=form)
        
        
    
#User class
class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id

    # Overriding object id to get the user id 
    def get_id(self):
        object_id = self.user_id.get('_id')
        return str(object_id)
    
# User login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        user = users.find_one({'username':request.form['username']})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            # Create a custom loginuser class to pass it to user to get is_active
            loginuser = User(user)
            login_user(loginuser, remember=form.data)
            flash('Welcome {}, you are logged in!'.format(form.username.data), 'success')
            return redirect(url_for('recipes'))
        else:
            flash('Please check your details and try again', 'danger')
    return render_template('login.html', page_title='User Login', form=form)
            
    

   
#User logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
    
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
