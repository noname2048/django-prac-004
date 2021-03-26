from django.core.management import BaseCommand, CommandParser
from accounts.models import User
from django.conf import settings
from faker.factory import Factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

Faker = Factory.create
fake = Faker("en_US")
fake.seed(1)


class Command(BaseCommand):
    help = "create some users"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("user_size", type=int)

    def handle(self, *args, **options):
        if settings.DEBUG == False:
            print("this command can be used when using debug mode. ")
            return 0

        user_size = options["user_size"]

        if not type(User) == type(get_user_model()):
            print("user model settings are diffent. (error)")
            return 0

        if user_size >= 1:
            print(f"create some users, size: {user_size}")

            count = User.objects.count()

            print(f"count: {count}")

            new_user_list = [
                User(
                    username=fake.user_name(),
                    email=fake.email(),
                    password=make_password("user"),
                    is_active=True,
                )
                for _ in range(count + user_size)
            ][count : count + user_size]

            print(new_user_list)

            for i, user in enumerate(new_user_list):
                u = User.objects.create_user(user)

            print("done.")
        else:
            print("parameter user_size must > 0")
