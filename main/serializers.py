from main.models import Message, Identity, MessageEncryptionIndicator
from rest_framework import serializers


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = '__all__'


class IdentitySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Identity
        fields = '__all__'


class MessageEncryptionIndicatorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = MessageEncryptionIndicator
        fields = '__all__'
