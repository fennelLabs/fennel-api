from main.models import Identity, Message, MessageEncryptionIndicator
from main.serializers import (
    IdentitySerializer,
    MessageSerializer,
    MessageEncryptionIndicatorSerializer,
)
from rest_framework import viewsets
import django_filters.rest_framework


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        queryset = Message.objects.all()
        recipient = self.request.query_params.get('recipient')
        sender = self.request.query_params.get('sender')
        if recipient is not None:
            queryset = queryset.filter(recipient__pk=recipient)
        if sender is not None:
            queryset = queryset.filter(sender__pk=sender)
        return queryset


class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        queryset = Identity.objects.all()
        fingerprint = self.request.query_params.get('fingerprint')
        if fingerprint is not None:
            queryset = queryset.filter(fingerprint=fingerprint)
        return queryset


class MessageEncryptionIndicatorViewSet(viewsets.ModelViewSet):
    queryset = MessageEncryptionIndicator.objects.all()
    serializer_class = MessageEncryptionIndicatorSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
