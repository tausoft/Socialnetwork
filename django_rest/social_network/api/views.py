from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from social_network.models import Messages
from .serializers import MessagesSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all().order_by("-created_at")
    lookup_field = "id"
    serializer_class = MessagesSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save()