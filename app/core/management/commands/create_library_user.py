# encoding: utf-8
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        try:
            user = User.objects.get(email="library.user@example.com")
            self.stdout.write("Library user exist!")
        except:
            user = User()
            user.username = "librayuser"
            user.email = "library.user@example.com"
            user.first_name = "Library"
            user.last_name = "User"
            user.set_password("user123")
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()
            self.stdout.write("Library user created!")
        finally:
            pass
