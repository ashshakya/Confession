from django.contrib.auth import authenticate

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .serializers import RegisterSerializer, TokenSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class RegisterationView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    data = {
                        'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                        'email': serializer.data.get('email', ''),
                        'username': serializer.data.get('username', ''),
                        'success': True
                    }
                    serializer = TokenSerializer(data=data)
                    if serializer.is_valid():
                        return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED
                        )
            else:
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            data = {
                'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                'username': username,
                "user_id": user.id,
                'success': True
            }
            serializer = TokenSerializer(data=data)
            if serializer.is_valid():
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'Email or Password not correct.'},
                status=status.HTTP_401_UNAUTHORIZED
            )