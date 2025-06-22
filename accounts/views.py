from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated  
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "full_name": user.get_full_name(),  
            "email": user.email,
            "birth_date": getattr(user, "birth_date", ""),  
        }
        return Response(data)

    def put(self, request):
        user = request.user
        data = request.data

        user.email = data.get("email", user.email)
        full_name = data.get("full_name", "")
        if full_name:
            parts = full_name.split(" ", 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ""
        if "birth_date" in data:
            user.birth_date = data["birth_date"]  
        if data.get("password"):
            user.set_password(data["password"])

        user.save()
        return Response({"detail": "Perfil atualizado com sucesso!"})