from gitsearch.celery import app
import json
import requests


@app.task
def create_users_from_git_filter(pk):
    from user.models import ApiSearchDetail, GithubUser

    #GithubUser.objects.update_or_create()

    try:
        details = ApiSearchDetail.objects.get(pk=pk).api_response
        users = json.loads(details)['items']
        for user in users:
            url = 'https://api.github.com/users/%s' % user['login']
            headers = {'Authorization': 'token 7ab8b09d4521304034626bf64bc03449095a217c'}
            try:
                git_response = requests.get(url, headers=headers)
                user_update = git_response.json()
                GithubUser.objects.update_or_create(login= user['login'], defaults=user_update)
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))
    print('Hello %s' % str(pk))
    return True