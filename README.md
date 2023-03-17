# TeamFriday :)

## Before you get started 

After cloning go into the `/TeamFriday-/oursite/` directory and make sure to ```pip install django-crispy-forms``` [(docs)](https://django-crispy-forms.readthedocs.io/en/latest/install.html), otherwise you will run into an error when running the server.

## How to contribute
To keep track of our changes and avoid "pushing to main", we can use sepearte branches for each of us, or alternatively, the feature we are working on.

## Making a new branch
- On the main repo page, select the branch dropdown and press 'view all branches'.
- Next select 'create new branch' and give it a name of your choosing.
- In an open terminal in the working directory of the project, type 'git pull' to pull new changes, then 'git checkout [your branch name]'.
- Now when you type 'git status' your branch should be selected and you can push your changes with no worries.

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

## Notes
At the moment we only have a main app to render some styled templates, but we will add more apps to handle user registration and crud fuctionality for this delivery.

## Todo
- user registration app -> custom user models, 2 sign-up pages and 1 login page.
- main app -> Course summary view with CRUD fuctionality, instructor/admin and student should render same page but with different buttons
- main app -> Application view for instructor/admin and students similar to ^^^
