from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Ad
from .serializers import *
from rest_framework import generics
from .api_response import post_add_response, get_all_response, get_ping_response, post_substract_response, \
    post_status_response


class AllView(APIView):
    def get(self, request, offset, amount):
        return get_all_response(request, offset, amount)


class PingView(APIView):
    def get(self, request):
        return get_ping_response(request)


class AddView(APIView):
    def post(self, request):
        return post_add_response(request)


class SubstractView(APIView):
    def post(self, request):
        return post_substract_response(request)


class StatusView(APIView):
    def post(self, request):
        return post_status_response(request)

