from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User, Token
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if phone and password:
            try:
                user = User.objects.get(phone=phone)
                if check_password(password, user.password):
                    Token.objects.filter(user=user).delete()
                    token_key = get_random_string(length=40)
                    expires_at = timezone.now() + datetime.timedelta(weeks=1)
                    token = Token.objects.create(key=token_key, user=user, expires_at=expires_at)
                    serializer = UserSerializer(user).data

                    return Response({'token': token.key, 'user': serializer}, status=status.HTTP_200_OK)


                else:
                    return Response({'error': 'Неверный телефон или пароль.'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь с таким телефоном не найден.'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Пожалуйста, предоставьте телефон и пароль.'}, status=status.HTTP_400_BAD_REQUEST)