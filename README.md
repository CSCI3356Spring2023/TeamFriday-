# TeamFriday :)

## Hello world


## Before you get started 

After cloning go into the `/TeamFriday-/oursite/` directory and make sure to ```pip install django-crispy-forms``` [(docs)](https://django-crispy-forms.readthedocs.io/en/latest/install.html), otherwise you will run into an error when running the server.

## Running the server

In the ./oursite directory run ```python manage.py runserver```

## CSS

Our styles.css file is located in `./oursite/main/static/`

## HTML

Our main templates are located in `./oursite/main/templates/main`

## Notes
At the moment we only have a main app to render some styled templates, but we will add more apps to handle user registration and crud fuctionality for this delivery.

## Todo
- user registration app -> custom user models, 2 sign-up pages and 1 login page.
- main app -> Course summary view with CRUD fuctionality, instructor/admin and student should render same page but with different buttons
- main app -> Application view for instructor/admin and students similar to ^^^
