# Git User searching 

How to setup
- Take the git pull 
- Create virtual environment
- Install all pip packages (pip install -U -r requirements.txt)
- Run the makemigrations and migrate commands(./manage makemigrations ./manage migrate)
- Create superuser to access Django admin(./manage createsuperuser)
- run celery worker to exceute the background job (`celery -A gitsearch worker`)


# API

- http://127.0.0.1:8000/api/v1/user/search?q=ravi&page=2&sort=username
- GitHub Token is used to hit Github API services, You can find that in user/constants.py
