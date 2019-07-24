from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, MultipleFileField, widgets
from wtforms.validators import DataRequired, Length, EqualTo, Email


#User registration form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=15)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message= 'Password do not match')])
    submit = SubmitField('Sign UP')
    
    
#User login form 
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = StringField('Remember Me')
    submit = SubmitField('Login')
    
    
# Variable declaration for the Allergens SelectMultipleField 
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


#Add recipe form
class AddRecipeForm(FlaskForm):
    image = StringField('Recipe Picture', validators=[DataRequired()])
    name = StringField('Recipe Name', validators=[DataRequired()])
    notes = StringField('Short Description', validators=[DataRequired()])
    author = StringField('Author Name', validators=[DataRequired()])
    course = SelectField('Course', choices= [('main','Main'), ('starter','Starter'),('salad','Salad'),('dessert','Dessert')] ,validators=[DataRequired()])
    cuisine = StringField('Cuisine', validators=[DataRequired()])
    string_of_files = ['Egg\r\nBacon\r\nPepper\r\nNutmeg\r\nSeafood\r\nTurmeric']
    list_of_files = string_of_files[0].split()
    files = [(x, x) for x in list_of_files]
    allergens = MultiCheckboxField('Allergens', choices=files, render_kw={"placeholder": "Choose..."})
    ingredient = StringField('Ingredients', validators=[DataRequired()])
    step = StringField('Preparation Steps', validators=[DataRequired()])
    submit = SubmitField('Submit')