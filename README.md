# EagleHire
## TeamFriday :)

![EagleHire](https://user-images.githubusercontent.com/87817813/226792489-a27d3ec0-9687-4cad-81d9-fdc258267732.PNG)




## To run the repo

After cloning go into the `/TeamFriday-/oursite/` directory and make sure to: ```pip install django-crispy-forms``` [(docs)](https://django-crispy-forms.readthedocs.io/en/latest/install.html),``` pip install django-multiselectfield```[(docs)](https://pypi.org/project/django-multiselectfield/), ``` pip install crispy-bootstrap4``` otherwise you will run into an error when running the server.

## Some Git review/tips
- It's a good rule of thumb to keep note of your current branch and if you are ahead/behind the branch before doing anything.
- "git pull" updates your current repo with new changes depending on your selected branch. Good to do this before making changes.

Will be used often to update your branch:
- "git add" stages your changes.
- "git commit -m [message]" creates the commit.
- "git push" effectively sends your commit and all it's changes to your current branch.

## Running the server

In the ./oursite directory run ```python manage.py runserver```.

## Migrations
If you make any changes to data models or anything db related, In the ./oursite directory run ```python manage.py makemigrations```.
Then you can migrate by running ``python manage.py migrate```.

## CSS

Our styles.css file is located in `./oursite/main/static/`.

## HTML

Our main templates are located in `./oursite/main/templates/main`.

