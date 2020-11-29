# !DO NOT WORK IN MASTER BRANCH! 
# - Used for production only

# Setup
#### Backend:
- Linux Machine: 
	1. Check your python version with `python --version`. If it is at least 3.6, then you are fine. If not, install python with `sudo apt-get install python3.6`.
	2. Install *pip* with `sudo apt-get install python3-pip`
	3. Install *virtualenv* with `sudo pip3 install virtualenv`
	4. Run `virtualenv venv; source venv/bin/activate`. To deactivate virtualenv, just run `deactivate`
		-	If you already ran the `virtualenv venv` command, then all you need to do is run `source venv/bin/activate`
	5. Install dependencies `pip3 install -r requirements.txt`
  6. IMPORTANT FOR LOCAL DEVELOPMENT:
    - Put the provided local.py in ./app/settings/
    - Put the provided local.sh in ./
    - in ./ , enter `source local.s`" inside console
	6. Enter `migrate` inside console
	7. Then enter `run` inside console and you can access the api at `localhost:8000/api/disaster-broadcaster/{endpoint}`

# Admin User:
Once the server is running and is in app directory, do:

1. Enter `createsuperuser` inside console
2. Input valid username, email, and password
3. Go to "http://localhost:8000/api/admin/" to sign in

Now, you have access to all data and tables as Django's superuser.

#### Note: Django admin requests differently from Postman. Django admin uses admin.ModelAdmin's def save_model() inside admin.py except when overriden, NOT by going through views->serializers.
#### Django admin is only for convenient data input by developers, frontend requests shall go through views->serializers instead.
