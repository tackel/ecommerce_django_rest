from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
#from django.contrib.sessions.models import Sessions
#from datetime import datetime
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.api.serializers import (CustomUserSerializer, CustomTokenObtainPairSerializer)
from apps.users.models import User


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login_serializer = self.serializer_class(data=request.data, context = {'request': request}) #el serializador serializer_class ya viene definido en Obtainauthtoken. y tiene dos campos: username y password
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0)) # el id 0 nunca existira
        if user.exists():
            RefreshToken.for_user(user.first())#refresh refresca el token pero no elimina el aterior, este sigo funcionando 
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)


'''
# ya no funciona con la interfaz de django, usar posman u otro
class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request': request} )     #el serializador serializer_class ya viene definido en Obtainauthtoken. y tiene dos campos: username y password
        #este serializador ya nos devuelve el user, en login_serializer.validated_data['user']
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user= user)
                user_serializer = CustomUserSerializer(user)
                if created:
                    return Response({
                        "token": token.key,
                        'user': user_serializer.data,
                        'message':'Inicio de sesion realizado.'
                    }, status=status.HTTP_201_CREATED)
                else:
                    
                    #si no queremos que entren en dos lugares distintos se puede borrar el token cuando se detecta 
                    all_sessions = Session.objects.filter(expire_date_gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete() # por que si quiere iniciar sesiond e otro navegador entra dos veces
                    token = Token.objects.create(user = user)
                    return Response({
                        "token": token.key,
                        'user': user_serializer.data,
                        'message':'Inicio de sesion realizado.'
                    }, status=status.HTTP_201_CREATED)
                    
                    # si lo que queremos es no permitir un segundo logueo si ya hay alguien logueado
                    token.delete()
                    return Response({"error":"Ya se ha iniciado sesion con este usuario"},
                    status=status.HTTP_409_CONFLICT
                    )


            else:
                return Response({'Error':'Este usuario no puede iniciar sesion'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Error':'Nombre de usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
          
        return Response({'mensaje':'Hola desde el response'}, status=status.HTTP_200_OK)
'''


