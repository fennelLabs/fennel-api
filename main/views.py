from main.models import Identity, Message, MessageEncryptionIndicator
from main.serializers import (
    IdentitySerializer,
    MessageSerializer,
    MessageEncryptionIndicatorSerializer,
)
from rest_framework import viewsets


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer


class MessageEncryptionIndicatorViewSet(viewsets.ModelViewSet):
    queryset = MessageEncryptionIndicator.objects.all()
    serializer_class = MessageEncryptionIndicatorSerializer
