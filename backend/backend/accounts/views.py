from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import RegisterSerializer
from rest_framework import viewsets
from rest_framework import status


class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    