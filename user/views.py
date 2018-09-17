from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from user.models import ApiSearchDetail, GithubUser
from django.db.models import Count
from user.constants import GITHUB_TOKEN
from urllib.parse import urlencode
import datetime


class GitUsersView(APIView):

    def get(self, request):
        query_params = dict()
        query = request.GET.get('q', None)
        sort = request.GET.get('sort', 'username')
        page = request.GET.get('page', 1)

        if query is None:
            return Response(
                status=getattr(status, 'HTTP_400_BAD_REQUEST'),
                data={'error': 'No search params'},
                content_type='application/json'
            )

        if sort:
            query_params.update({'sort': sort})
        if page:
            query_params.update({'page': page})
        query_params.update({'q': query})

        url = 'https://api.github.com/search/users?%s' % urlencode(query_params)
        headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
        try:
            git_response = requests.get(url, headers=headers)

            ApiSearchDetail.objects.create(query_params=urlencode(query_params), api_response=json.dumps(git_response.json()))
            return Response(
                status=getattr(status, 'HTTP_200_OK'),
                data=git_response.json(),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                status=getattr(status, 'HTTP_400_BAD_REQUEST'),
                data={'error': str(e)},
                content_type='application/json'
            )


class AdminReports(APIView):

    def get(self, request):
        today = datetime.datetime.now()

        if not request.user.is_superuser:
            return Response(
                    status=getattr(status, 'HTTP_400_BAD_REQUEST'),
                    data={'error':'Not an admin user.'},
                    content_type='application/json'
                )
        user_query_set = GithubUser.objects.all()
        total_user = user_query_set.count()

        user_today = user_query_set.filter(created_date__day=today.day).count()
        user_this_month = user_query_set.filter(created_date__month=today.month).count()
        user_this_year = user_query_set.filter(created_date__year=today.year).count()

        api_query_set = ApiSearchDetail.objects.all()
        total_api = api_query_set.count()
        total_api_day = api_query_set.filter(created_date__day=today.day).count()
        total_api_this_month = api_query_set.filter(created_date__month=today.month).count()
        total_api_this_year = api_query_set.filter(created_date__year=today.year).count()

        return Response(
            status=getattr(status, 'HTTP_200_OK'),
            data={
                'users': {
                    'total': total_user,
                    'user_today': user_today,
                    'user_this_month': user_this_month,
                    'user_this_year': user_this_year},
                'api': {
                    'total_api': total_api,
                    'total_api_day': total_api_day,
                    'total_api_this_month': total_api_this_month,
                    'total_api_this_year': total_api_this_year
                }
            },
            content_type='application/json'
        )
