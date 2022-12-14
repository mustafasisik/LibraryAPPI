# encoding: utf-8
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        try:
            user = User.objects.get(email="admin@example.com")
            self.stdout.write("Admin exist!")
        except:
            user = User()
            user.username = "admin"
            user.email = "admin@example.com"
            user.first_name = "Super"
            user.last_name = "User"
            user.set_password("admin123")
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write("Admin created!")
        finally:
            pass