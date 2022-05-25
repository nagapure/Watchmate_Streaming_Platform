from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# Logout view for user
@api_view(["POST"])
def logout_view(request):

    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(
            {"message": "User logout successfully"}, status=status.HTTP_200_OK
        )


# Registrations view for user
@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():

            account = serializer.save()
            print(account)

            data["response"] = "Registration Successful!"
            data["username"] = account.username
            data["email"] = account.email

            token = Token.objects.get(user=account).key
            data["token"] = token

            # Below code is for JWT authentication

            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }

        else:
            data = serializer.errors

        return Response(data, status = status.HTTP_201_CREATED)
