import json
from rest_framework.test import APIClient

from main.models import Identity


def test_get_identities():
    client = APIClient()
    Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    response = client.get("/api/identities/")
    Identity.objects.all().delete()
    assert response.status_code == 200
    assert len(list(json.loads(response.content.decode()))) == 1


def test_get_single_identity():
    client = APIClient()
    identity = Identity.objects.create(
        on_chain_identity_number=0,
        fingerprint="test",
        public_key="test",
        shared_secret_key="test",
    )
    response = client.get(f"/api/identities/{identity.pk}/")
    response_dict = json.loads(response.content.decode())
    print(response_dict)
    Identity.objects.all().delete()
    assert response_dict["id"] == identity.pk
    assert response_dict["fingerprint"] == identity.fingerprint


def test_post_identity():
    client = APIClient()
    response = client.post(
        "/api/identities",
        {
            "on_chain_identity_number": 0,
            "fingerprint": "test",
            "public_key": "test",
            "shared_secret_key": "test",
        },
    )
    Identity.objects.all().delete()
    assert response.status_code == 301
