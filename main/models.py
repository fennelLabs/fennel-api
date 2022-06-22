from django.db import models


class Message(models.Model):
    message = models.CharField(max_length=256)
    public_key = models.CharField(max_length=256)
    signature = models.CharField(max_length=256)
    fingerprint = models.CharField(max_length=256)
    sender = models.ForeignKey(
        "Identity", related_name="sender", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        "Identity", related_name="recipient", on_delete=models.CASCADE
    )
    message_encryption_indicator = models.ForeignKey(
        "MessageEncryptionIndicator", on_delete=models.CASCADE
    )


class Identity(models.Model):
    on_chain_identity_number = models.IntegerField()
    fingerprint = models.CharField(max_length=256)
    public_key = models.CharField(max_length=256)
    shared_secret_key = models.CharField(max_length=256)


class MessageEncryptionIndicator(models.Model):
    name = models.CharField(max_length=128)
