from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Books
from .serializers import UserRegistrationSerializer, UserLoginSerializer, CustomTokenObtainPairSerializer, \
    BooksSerializer


# Create your views here.

class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            return Response({'refresh': str(refresh),
                             'access': str(refresh.access_token), 'msg': 'Registration Successful'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                refresh = CustomTokenObtainPairSerializer.get_token(user)
                return Response({'refresh': str(refresh),
                                 'access': str(refresh.access_token), 'msg': 'Login Successful'})
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}})


class BooksListView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data)


class BooksUploadingView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.role == 'admin':
            serializer = BooksSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Book Added Successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Not an admin Member'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        user = request.user
        if user.role == 'admin':
            books = Books.objects.get(pk=pk)
            serializer = BooksSerializer(books, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'message': 'Not an admin user'})

    def patch(self, request, pk):
        user = request.user
        if user.role == 'admin':
            books = Books.objects.get(pk=pk)
            serializer = BooksSerializer(books, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({'message': 'Not an admin user'})

    def delete(self, request, pk):
        user = request.user
        if user.role == 'admin':
            books = Books.objects.get(pk=pk)
            books.delete()
            return Response({'message': 'Book deleted successfully'})
        else:
            return Response({'message': 'Not an admin user'})
