# My Cookbook 

A project created to organizing recipes where would be possible to perform actions accordingly to the user needs.
The main objective was to focus in the use of Python, Flask and MongoDB .

## UX

This website was created specially for the lover's of cooking, for the ones who's might have lots of time to be in the kitchen or for the ones who needs to rush because of the busy life of these days but still rather then go for a fast food on their way to work, prefer to cook a quick and delicious dish to take with then.
After all eating healthy is the only way if you want to live "forever" .

• As a user, you will be able to browser through all the recipes in the database.
    
• As a user, you will have access to a variety of recipes from all over the world.

• As a user, you will be able to choose from different recipes categories.

• As a user, you will be able to search before hand for recipes that contain some allergens, so that you can have the option of avoid then.

• As a user, you will be able to choose your favorite author from the author list.

• As a user, you will be able to express your option trough a like button. 

• As a user, you will be able to add your own recipe.

• As a user, you will have the freedom to edit your recipe whenever you like.

• As a user, you will be able to delete a recipe.

• The wireframe for this project can be accessed here https://github.com/Luciano-Lima/myCookbook/blob/master/cookbook.png

## Features

### Existing Features

• From the website home page you can navigate trough the mains links directing you to a specific page.

• You can also from the home page use the link to Sign UP and create an account.

• From the navigation menu you can follow the link to add your own recipe, register, login or logout.

• From the main page session at the top you will find a navigation where you will be able to filter the recipes accordingly  to courses, cuisine, allergens or author.

• Bellow you will have displayed all the recipes without any filter.  

• In the footer session you will find a social links where you can share your favorite recipe.

• If you want to know more  about a specific recipe you can click on it and you will be redirected to the recipe full description page.

• From the single recipe page at the bottom of the page you will find a button to edit or delete the recipe.

### Features to be Implement

• A newsletter announcing about the new added recipes.

• A video playlist teaching the cooking preparation steps.

• An authentication system preventing unauthorized user to edit or delete recipes that are not there own.

• A counter for the like bottom the doesn't reset on page load.



## Technologies Used

<a href="https://dev.w3.org/html5/html-author/">HTML</a> - Mark-up language for the structure and presentation of the contents.

<a href="https://www.w3.org/Style/CSS/Overview.en.html">CSS</a> - To add style to the web documents

<a href="https://jquery.com/">JQuery</a> - To simplify the DOM manipulation.

<a href="https://getbootstrap.com/">Bootstrap</a> - For responsive grid layout.

<a href="https://flask.palletsprojects.com/en/1.1.x/">Flask<a/> - A micro framework for Python to building a complex database-driven website. 

<a href="http://jinja.pocoo.org/docs/2.10/">Jinja2<a/> - A Templating language for Python

<a href="https://aws.amazon.com/cloud9/?origin=c9io">Cloul9<a/> - AWS Cloud9 is a cloud-based integrated development environment (IDE) 

<a href="https://wtforms.readthedocs.io/en/stable/">WTForms<a/> - A flexible forms validation and rendering library for Python

<a href="https://www.python.org/">Python</a>  -  A program language

<a href="https://www.mongodb.com/">MongoDB<a/>A document based database used for general purpose, built form modern applications.

## Testing


This project has manual testing and it was tested in all the major browsers including Google Chrome, Safari and Internet Explorer to confirm compatibility.
I have conducted tests in virtual mode using the google developer tools and also physical mobile phones including Nokia, Samsung Galaxy, HtcM8, Samsung Tablet S4,   IPad and IPhone5 to check that the website has a mobile friendly design and it does work in all platforms.

I have used the https://validator.w3.org/ to validate the HTML code and corrected all the major error or warning messages.
I have uploaded the CSS file to https://jigsaw.w3.org/css-validator/validator to check for error and the result was clear, no error or warning was detected, except for error relate to bootstrap.min.css.
Each of the navigation links including the social links in the footer was tested simulating an logged in and/or logged out user to make sure it  does redirects to the correspondent page.

Home page will display the navigation links at the top which could direct the user to the recipe page or where to login or to register. Also a  welcome message. On the mobile version I have also included icons to display with each of the nav links.

The Browse Recipes filter functionality which does not required a user to be logged in can be found on the recipes page, it  can filter the database and return  individual results by selecting only one option from: Course - Cuisine - Allergens - Author or if multiple categories were selected it  will return all the items that match the selected filters and display to the user.

The form on the register page will enable the user to register so they can add their own recipes to the database. The form was tested to make sure the user  have a username, email and password. The form will not be submitted if a field is left blank or doesn’t match the required parameters which in case of an error it will display a message telling to the user what needs to be corrected before the form  submission. Also was tested to make sure it does displays a message error in case the user already exists. 

The login form was tested in the same way as the register page to make sure it does display an error message in case the details entered by the user are incorrect. Also to make  sure the logged in user are redirected to the recipes page.

Add recipe form, similar as all forms, was tested to make sure no fields are left blank or has incorrect input. It will display a message error in case the information entered by the user doesn’t match the required fields or left blank.  The button to add or remove additional ingredients or step preparation were tested adding and removing multiple times information to the fields and it does work as it should, so if the user changes his/her mind and doesn't want to add the last ingredient field he/she can click on the (-) button to remove the last field.

The arrow sign displayed at the bottom right of the page was tested on desktop and mobile versions to make sure it does scroll up smoothly  to the top of the page.

During the development of this project I have founded some bugs, some of them were simple to work around and to get the best solution, form example: 

Imagens alignment: which were fixed applying a fixed height to the cards.

Forms fields for ingredients and preparations steps on the edit recipe form uses an auto increment button, it wasn't saving the inputs into the database. The bug was fixed adding an extra loop on Jinja template to the edit recipe form to render inputs for the those fields and also adding a class to ''name" named ingredients.

At the beginning of this project every user were be able to add, edit or delete recipes which could result in the loss of all database information. The ability to hide contents for a user that does have credentials was fixed adding a register system so only logged in user can now see this content. 

## Deployment

To see the code follow the link to my GitHub repository. https://github.com/Luciano-Lima/myCookbook . If you like you can also download or clone the repo, just click on the green "Clone or Download button" then save it to a folder in you computer.
The website is hosted on Heroku. Here is the live version link:  https://my-cook-book.herokuapp.com/

To deploy the project to heroku I have used the following commands from the Cloud9 terminal:

Login to Heroku: heroku login

Enter your credentials: email and password

Create you app:  heroku create follow by the "name of your project".

Before we push to heroku we need to set the config Vars.

Push to heroku:  git push -u heroku master

To see the list of your apps: heroku apps

From  Heroku you go to settings and click on config vars that will allow you to connect the app to heroku.
You can edit your app name.
You will need to specify the IP - MONGO_URI - PORT to connect the app from cloud9 to heroku.

The environment variables used in this project were saved in the bash directory. 
During the development phase the debug mode were set to True so that would help to identify and correct any bugs.
For deployment the debug were set to False that will also enable increasing in the app performance.

### The Database

The database I have chosen to work with this project was MongDB a no relational database, that stores data in JSON format.
The database structure was constructed mainly including arrays and strings in a non relational data structure. 


## Credits

### Content & Media

• The recipes data including some of the pictures used in this project were from https://github.com/LeaVerou

• I have used as example to complete this project a website like https://www.epicurious.com/

• I have also used Corey Schafer tutorials as an example to implement the login system.  https://www.youtube.com/user/schafer5
