from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializers
from django.contrib.auth.models import User, Permission
from rest_framework.authtoken.models import Token
from rest_framework import status

class userViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login endpoint"""
        user = get_object_or_404(User, username=request.data['username'])

        if not user.check_password(request.data['password']):
            return Response({"error": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        serializer = UserSerializers(instance=user)

        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        """User registration endpoint"""
        serializer = UserSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=serializer.data['username'])
            user.set_password(request.data['password'])
            user.save()

            role = request.data.get('role')  # 'mesero', 'cocina', 'caja', 'admin'
            if role:
                perm_codename = f"{role}_access"
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    user.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    return Response({'error': 'Permiso no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)