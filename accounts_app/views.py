from django.contrib.auth import authenticate
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserSignUpView(APIView):

    def post(self, request):
        request.data["username"] = request.data["email"]
        user = User.objects.create_user(**request.data)
        token = Token.objects.create(user=user)
        return Response(
            {"user": user.email, "token": token.key}, status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"user": user.email, "token": token.key})
        else:
            return Response(
                "No user matching credentials", status=status.HTTP_404_NOT_FOUND
            )


class UserDetailView(APIView):

    def get(self, request):
        return Response({"email": request.user.email})


class UserLogOutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUserCreate(APIView):

    def post(self, request):
        request.data["username"] = request.data["email"]
        admin_user = User.objects.create_user(**request.data)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_staff_member = True
        admin_user.save()
        token = Token.objects.create(user=admin_user)
        return Response(
            {"admin_user": admin_user.email, "token": token.key},
            status=status.HTTP_201_CREATED
        )
