from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token


class RegisterAccount(APIView):
    def post(self, request, *args, **kwargs):

        if {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):

            try:
                validate_password(request.data['password'])
            except Exception:
                return JsonResponse({'Status': False, 'Error': 'Создайте пароль отвечающий требованиям'})

            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                user.set_password(request.data['password'])
                user.save()

                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        else:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class LoginAccount(APIView):
    def post(self, request, *args, **kwargs):

        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])

            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)

                    return JsonResponse({'Status': True, 'Token': token.key})

            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
