import json
from rest_framework.test import APIClient

from main.models import Message, Identity, MessageEncryptionIndicator


def test_get_messages():
    client = APIClient()
    identity = Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    indicator = MessageEncryptionIndicator.objects.create(name="Test Indicator")
    Message.objects.create(
        message="Test Message",
        public_key="pubkey",
        signature="sign(Test Message)",
        fingerprint="test",
        sender=identity,
        recipient=identity,
        message_encryption_indicator=indicator,
    )
    response = client.get("/api/messages/")
    Message.objects.all().delete()
    Identity.objects.all().delete()
    MessageEncryptionIndicator.objects.all().delete()
    assert response.status_code == 200
    assert len(list(json.loads(response.content.decode()))) == 1


def test_filter_messages():
    client = APIClient()
    identity = Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    identity2 = Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    indicator = MessageEncryptionIndicator.objects.create(name="Test Indicator")
    Message.objects.create(
        message="Test Message",
        public_key="pubkey",
        signature="sign(Test Message)",
        fingerprint="test",
        sender=identity,
        recipient=identity,
        message_encryption_indicator=indicator,
    )
    Message.objects.create(
        message="Test Message 2",
        public_key="pubkey",
        signature="sign(Test Message)",
        fingerprint="test",
        sender=identity,
        recipient=identity2,
        message_encryption_indicator=indicator,
    )
    response = client.get(f"/api/messages/?recipient={identity.pk}")
    print(response.content)
    Message.objects.all().delete()
    Identity.objects.all().delete()
    MessageEncryptionIndicator.objects.all().delete()
    assert response.status_code == 200
    assert len(list(json.loads(response.content.decode()))) == 1


def test_get_single_message():
    client = APIClient()
    identity = Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    indicator = MessageEncryptionIndicator.objects.create(name="Test Indicator")
    message = Message.objects.create(
        message="Test Message",
        public_key="pubkey",
        signature="sign(Test Message)",
        fingerprint="test",
        sender=identity,
        recipient=identity,
        message_encryption_indicator=indicator,
    )
    response = client.get(f"/api/messages/{message.pk}/")
    response_dict = json.loads(response.content.decode())
    print(response.content)
    Message.objects.all().delete()
    Identity.objects.all().delete()
    MessageEncryptionIndicator.objects.all().delete()
    assert response_dict['id'] == message.pk
    assert response_dict['message'] == message.message


def test_post_message():
    client = APIClient()
    identity = Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    indicator = MessageEncryptionIndicator.objects.create(name="Test Indicator")
    response = client.post("/api/messages", {
        'message': 'ciphertext',
        'public_key': 'publicKey',
        'signature': 'signature',
        'fingerprint': 'fingerprint',
        'sender': f'/api/identities/{identity.pk}/',
        'recipient': f'/api/identities/{identity.pk}/',
        'message_encryption_indicator': f'/api/message_encryption_indicators/{indicator.pk}/'
      }, format='json')
    Message.objects.all().delete()
    Identity.objects.all().delete()
    MessageEncryptionIndicator.objects.all().delete()
    assert response.status_code == 301
