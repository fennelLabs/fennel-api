from django.contrib import admin
from .models import Message, Identity, MessageEncryptionIndicator


admin.site.register(Message)
admin.site.register(Identity)
admin.site.register(MessageEncryptionIndicator)
