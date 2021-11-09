from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework import generics, viewsets
from .models import User

class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        obj = generics.get_object_or_404(User.objects.filter(id=self.kwargs["pk"]))
        self.check_object_permissions(self.request, obj)
        return obj

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer

class LoginAPIView(TokenObtainPairView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

