from django.core.management import BaseCommand, CommandParser
from ....accounts.models import User
from django.conf import settings


class Command(BaseCommand):
    help = "create superuser"

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            user = settings.FIRST_USER
            username = user["username"]
            email = user["email"]
            password = user["password"]

            print(f"Create Superuser for {username} ({email})")
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()

            print("superuser created")
        else:
            print("superuser already exist")
