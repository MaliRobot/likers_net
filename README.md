
# Likers Net 

## Awesome Django social app for hackers and bots alike using REST!

### Features
- Create user accounts
- Write posts
- Like posts by other users
- Authenticate using JWT
- Use hunter.io to validate user's emails
- Take advantage of Clearbit to get info on user's company from email data

## Get up and running

1. Clone this repo
2. Create a virtual environment:

```
cd likers_net
python -m venv .venv
```

3\. Activate the virtual environment:

```
source .venv/bin/activate
```

4\. Install the requirements:

```
pip install -r requirements.txt
```

5\. Create a file named `.env`

Inside add:
```
SECRET_KEY=<insert your django secret key>
DB_NAME=<db name>
DB_USER=<db user>
DB_PASS=<db password>
DEBUG=<1 for true 0 for false, if debug 1, clearbit and hunter are not used>
HUNTER_KEY=<your hunter key>
CLEARBIT_KEY=<your clearbit key>

# bot parameters
NUMBER_OF_USERS=<desired number of users to be created>
MAX_POSTS_PER_USER=<maximum number of posts>
MAX_LIKES_PER_USER=<maximum likes per user>
BASE_URL=<url and port such as localhost:8000>
```

NOTE:

For more information on how you can generate a secret key visit [here](https://foxrow.com/generating-django-secret-keys) or you can generate a key online at [here](https://www.miniwebtool.com/django-secret-key-generator/).
If debug is set to 1 Clearbit and Hunter wont be used saving you the number of calls you have available on your account.

6\. Run migrations:

```
python manage.py migrate
```

7\. Get the server up and running:

```
python manage.py runserver
```

8\. Run bot to check out Likers net features (run in parallel with runserver)

```
python manage.py bot
```
