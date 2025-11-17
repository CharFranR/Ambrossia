from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User, Permission
from rest_framework.authtoken.models import Token
from .serializers import UserSerializers


class userViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar operaciones de usuarios (login y registro).
    """

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Endpoint para login de usuarios.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "username y password son requeridos"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            return Response(
                {"error": "invalid password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializers(instance=user)

        return Response(
            {"token": token.key, "user": serializer.data}, 
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Endpoint para registro de nuevos usuarios.
        Permite asignar permisos personalizados basados en roles.
        """
        serializer = UserSerializers(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # Validar que user es instancia de User
            if isinstance(user, User):
                role = request.data.get('role')
                if role:
                    perm_codename = f"{role}_access"
                    try:
                        perm = Permission.objects.get(codename=perm_codename)
                        user.user_permissions.add(perm)
                    except Permission.DoesNotExist:
                        return Response(
                            {'error': 'Permiso no existe'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No se pudo crear el usuario correctamente'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)