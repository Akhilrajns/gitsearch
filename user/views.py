from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from user.models import ApiSearchDetail, GithubUser
from django.db.models import Count
from django.http import HttpResponse


class GitUsersView(APIView):

    def get(self, request):
        url = 'https://api.github.com/search/users?q=%s' % 'akhil'
        headers = {'Authorization': 'token 7ab8b09d4521304034626bf64bc03449095a217c'}
        try:
            git_response = requests.get(url, headers=headers)

            ApiSearchDetail.objects.create(query_params='akhil', api_response=json.dumps(git_response.json()))
            return Response(
                status=getattr(status, 'HTTP_200_OK'),
                data=git_response.json(),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                status=getattr(status, 'HTTP_400_BAD_REQUEST'),
                data=str(e),
                content_type='application/json'
            )


def reports(request):

    if not request.user.is_superuser:
        return Response(
                status=getattr(status, 'HTTP_400_BAD_REQUEST'),
                data='Not an admin user.',
                content_type='application/json'
            )

    user_reports = GithubUser.objects.values('created_date__year', 'created_date__month', 'created_date__day').annotate(
        count=Count('pk'))

    api_reports = ApiSearchDetail.objects.values('created_date__year', 'created_date__month', 'created_date__day').annotate(
        count=Count('pk'))

    return Response(
        status=getattr(status, 'HTTP_200_OK'),
        data={'users': user_reports, 'api': api_reports},
        content_type='application/json'
    )
