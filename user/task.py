from gitsearch.celery import app
import json
import requests
from user.constants import GITHUB_TOKEN

@app.task
def create_users_from_git_filter(pk):
    from user.models import ApiSearchDetail, GithubUser

    try:
        details = ApiSearchDetail.objects.get(pk=pk).api_response
        users = json.loads(details)['items']
        for user in users:
            url = 'https://api.github.com/users/%s' % user['login']
            headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
            try:
                git_response = requests.get(url, headers=headers)
                user_update = git_response.json()
                fields = [f.name for f in GithubUser._meta.get_fields()]

                fields.remove('login')
                fields.remove('id')
                fields.remove('is_superuser')
                fields.remove('created_date')
                fields.remove('modified_date')
                fields.remove('is_staff')
                fields.remove('user_permissions')
                fields.remove('logentry')
                fields.remove('password')
                fields.remove('last_login')
                fields.remove('groups')

                defaults_keys = dict()
                for field in fields:
                    if field == 'score':
                        defaults_keys[field] = '0' if user_update.get(field) is None else user_update.get(field)
                    else:
                        defaults_keys[field] = '' if user_update.get(field) is None else user_update.get(field)
                GithubUser.objects.update_or_create(
                    login=user_update.get('login'),
                    defaults=defaults_keys
                )
            except Exception as e:
                print('Invalid Exception %s' % str(e))

    except Exception as e:
        print(str(e))
    return True