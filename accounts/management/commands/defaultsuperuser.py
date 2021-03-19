import logging
import os

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create a default superuser account'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def handle(self, *args, **options):
        logger = logging.getLogger('django')
        username = settings.DEFAULT_ADMIN_USERNAME
        email = settings.DEFAULT_ADMIN_EMAIL
        password = settings.DEFAULT_ADMIN_PASSWORD
        first_name = settings.DEFAULT_ADMIN_FIRST_NAME
        last_name = settings.DEFAULT_ADMIN_LAST_NAME

        try:
            if self.UserModel.objects.filter(username=username).exists():
                self.stderr.write('Superuser already exists.')
            else:
                user = self.UserModel.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                self.stdout.write('Superuser is successfully created.')
        except IntegrityError as error:
            logger.warning("DB Error Thrown %s" % error)
