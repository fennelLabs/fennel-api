import graphene
from graphene_django import DjangoObjectType

from .models import Message, Identity, MessageEncryptionIndicator


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = "__all__"


class MessageInput(graphene.InputObjectType):
    message = graphene.String()
    signature = graphene.String()
    fingerprint = graphene.String()
    public_key = graphene.String()
    sender = graphene.Int()
    recipient = graphene.Int()
    message_encryption_indicator = graphene.Int()


class CreateMessage(graphene.Mutation):
    class Arguments:
        input = MessageInput(required=True)

    message = graphene.Field(MessageType)

    @classmethod
    def mutate(cls, root, info, input):
        message = Message()
        message.message = input.message
        message.signature = input.signature
        message.fingerprint = input.fingerprint
        message.public_key = input.public_key
        message.sender = Identity.objects.get(pk=input.sender)
        message.recipient = Identity.objects.get(pk=input.recipient)
        message.message_encryption_indicator = MessageEncryptionIndicator.objects.get(
            pk=input.message_encryption_indicator
        )
        message.save()
        return CreateMessage(message=message)


class UpdateMessage(graphene.Mutation):
    class Arguments:
        input = MessageInput(required=True)
        id = graphene.ID()

    message = graphene.Field(MessageType)

    @classmethod
    def mutate(cls, root, info, input, id):
        message = Message.objects.get(pk=id)
        message.message = input.message
        message.signature = input.signature
        message.fingerprint = input.fingerprint
        message.public_key = input.public_key
        message.sender = Identity.objects.get(pk=input.sender)
        message.recipient = Identity.objects.get(pk=input.recipient)
        message.message_encryption_indicator = MessageEncryptionIndicator.objects.get(
            pk=input.message_encryption_indicator
        )
        message.save()
        return UpdateMessage(message=message)


class IdentityType(DjangoObjectType):
    class Meta:
        model = Identity
        fields = "__all__"


class IdentityInput(graphene.InputObjectType):
    fingerprint = graphene.String()
    public_key = graphene.String()
    shared_secret_key = graphene.String()


class CreateIdentity(graphene.Mutation):
    class Arguments:
        input = IdentityInput(required=True)

    identity = graphene.Field(IdentityType)

    @classmethod
    def mutate(cls, root, info, input):
        identity = Identity()
        identity.fingerprint = input.fingerprint
        identity.public_key = input.public_key
        identity.shared_secret_key = input.shared_secret_key
        identity.save()
        return CreateIdentity(identity=identity)


class UpdateIdentity(graphene.Mutation):
    class Arguments:
        input = IdentityInput(required=True)
        id = graphene.ID()

    identity = graphene.Field(IdentityType)

    @classmethod
    def mutate(cls, root, info, input, id):
        identity = Identity.objects.get(pk=id)
        identity.fingerprint = input.fingerprint
        identity.public_key = input.public_key
        identity.shared_secret_key = input.shared_secret_key
        identity.save()
        return UpdateIdentity(identity=identity)


class MessageEncryptionIndicatorType(DjangoObjectType):
    class Meta:
        model = MessageEncryptionIndicator
        fields = "__all__"


class MessageEncryptionIndicatorInput(graphene.InputObjectType):
    name = graphene.String()


class CreateMessageEncryptionIndicator(graphene.Mutation):
    class Arguments:
        input = MessageEncryptionIndicatorInput(required=True)

    message_encryption_indicator = graphene.Field(MessageEncryptionIndicatorType)

    @classmethod
    def mutate(cls, root, info, input):
        indicator = MessageEncryptionIndicator()
        indicator.name = input.name
        indicator.save()
        return CreateMessageEncryptionIndicator(message_encryption_indicator=indicator)


class UpdateMessageEncryptionIndicator(graphene.Mutation):
    class Arguments:
        input = MessageEncryptionIndicatorInput(required=True)
        id = graphene.ID()

    message_encryption_indicator = graphene.Field(MessageEncryptionIndicatorType)

    @classmethod
    def mutate(cls, root, info, input, id):
        indicator = MessageEncryptionIndicator.objects.get(pk=id)
        indicator.name = input.name
        indicator.save()
        return UpdateMessageEncryptionIndicator(message_encryption_indicator=indicator)


class Query(graphene.ObjectType):
    messages = graphene.List(MessageType)
    messages_from_user = graphene.List(MessageType)
    messages_to_user = graphene.List(MessageType)
    identities = graphene.List(IdentityType)
    message_encryption_indicators = graphene.List(MessageEncryptionIndicatorType)

    def resolve_messages(root, info, **kwargs):
        return Message.objects.all()
    
    def resolve_messages_from_user(root, info, user_id):
        return Message.objects.filter(sender__pk=user_id)
    
    def resolve_messages_to_user(root, info, user_id):
        return Message.objects.filter(recipient__pk=user_id)

    def resolve_identities(root, info, **kwargs):
        return Identity.objects.all()

    def resolve_message_encryption_indicator(root, info, **kwargs):
        return MessageEncryptionIndicator.objects.all()


class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
    update_message = UpdateMessage.Field()

    create_identity = CreateIdentity.Field()
    update_identity = UpdateIdentity.Field()

    create_message_encryption_indicator = CreateMessageEncryptionIndicator.Field()
    update_message_encryption_indicator = UpdateMessageEncryptionIndicator.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
