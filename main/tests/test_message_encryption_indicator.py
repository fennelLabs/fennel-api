import json
from rest_framework.test import APIClient

from main.models import MessageEncryptionIndicator


def test_get_message_encryption_indicators():
    client = APIClient()
    MessageEncryptionIndicator.objects.create(
        name="Test"
    )
    response = client.get("/api/message_encryption_indicators/")
    MessageEncryptionIndicator.objects.all().delete()
    assert response.status_code == 200
    assert len(list(json.loads(response.content.decode()))) == 1


def test_get_single_identity():
    client = APIClient()
    indicator = MessageEncryptionIndicator.objects.create(
        name="Test"
    )
    response = client.get(f"/api/message_encryption_indicators/{indicator.pk}/")
    response_dict = json.loads(response.content.decode())
    print(response_dict)
    MessageEncryptionIndicator.objects.all().delete()
    assert response_dict["id"] == indicator.pk
    assert response_dict["name"] == indicator.name


def test_post_identity():
    client = APIClient()
    response = client.post(
        "/api/message_encryption_indicators",
        {
            "name": "test",
        },
    )
    MessageEncryptionIndicator.objects.all().delete()
    assert response.status_code == 301
