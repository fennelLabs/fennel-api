"""
Defines a createadmin command extending manage.py.
"""

from django.core.management.base import BaseCommand
from main.models import MessageEncryptionIndicator

INDICATORS = [
    "Unencrypted",
]


class Command(BaseCommand):
    """
    Extends the BaseCommand class, providing tie-ins to Django.
    """

    def handle(self, *args, **options):
        """
        Carry out the command functionality.

        @param args:
        @param options:
        @return:
        """
        for indicator in INDICATORS:
            if not MessageEncryptionIndicator.objects.filter(name=indicator).exists():
                MessageEncryptionIndicator.objects.create(name=indicator)
