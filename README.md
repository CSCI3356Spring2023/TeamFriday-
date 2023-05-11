# EagleHire 
## by TeamFriday :)

![image](https://github.com/CSCI3356Spring2023/TeamFriday-/assets/87817813/4558bd7f-f413-4870-91c5-f6d44d4e8e74)

Introducing *EagleHire*, the newest solution for Boston College's Computer Science department. With faculty currently relying on Google Forms and email to hire TAs, there's an urgent need for a better and more efficient way to connect faculty and students. 

Developed using the powerful Python Django web framework, as well as HTML, CSS, and the Bootstrap CSS framework, EagleHire aims to make the hiring process easier and more streamlined for everyone involved. 

Say goodbye to tedious forms and endless email chains - with EagleHire, finding a TA position or hiring a TA has never been easier!
#

## Development Notes

After cloning/pulling new changes, go into the `/TeamFriday-/oursite/` directory and make sure to: 

- ```pip install django-environ```[(.env file for secret keys)](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f)
- ```pip install django-crispy-forms``` [(docs)](https://django-crispy-forms.readthedocs.io/en/latest/install.html)
- ```pip install django-multiselectfield```[(docs)](https://pypi.org/project/django-multiselectfield/) 
- ```pip install crispy-bootstrap4``` [(docs)](https://getbootstrap.com/docs/4.0/getting-started/introduction/) 

Otherwise you will run into an error when running the server. 
Additionally, if you run into any backend related errors with our tables, see Migrations below to keep the db up to date.

## Migrations

If you make any changes to data models or anything db related, In the ./oursite directory run ```python manage.py makemigrations```.
Then you can migrate by running ```python manage.py migrate```.

## Running the server

In the ./oursite directory run ```python manage.py runserver```.

## Some Git review/tips

- It's a good rule of thumb to keep note of your current branch and if you are ahead/behind the branch before doing anything.
- "git pull" updates your current repo with new changes depending on your selected branch. Good to do this before making changes.

Will be used often to update your branch:
- "git add" stages your changes.
- "git commit -m [message]" creates the commit.
- "git push" effectively sends your commit and all it's changes to your current branch.

## CSS

Our styles.css file is located in `./oursite/main/static/`.

## HTML

Our main templates are located in `./oursite/main/templates/main`.
