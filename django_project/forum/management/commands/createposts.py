from django.core.management import BaseCommand, CommandParser
from django.conf import settings
from faker.factory import Factory
from django.contrib.auth import get_user_model
from forum.models import ForumPost
import random

Faker = Factory.create
fake = Faker("ko_KR")
fake.seed(1)


class Command(BaseCommand):
    help = "create many posts"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("post_size", type=int)

    def handle(self, *args, **options):
        if settings.DEBUG == False:
            print("this command can be used when using debug mode. ")
            return 0

        post_size = options["post_size"]
        User = get_user_model()

        if post_size >= 1:
            print(f"create f{post_size} posts")

            user_cnt = User.objects.count()
            post_cnt = ForumPost.objects.count()

            if user_cnt < 1:
                print(f"no user exist")
                return 0

            new_post_list = [
                ForumPost(
                    author=random.choice(User.objects.all()[:3]),
                    title=fake.catch_phrase(),
                    content=fake.address(),
                )
                for _ in range(post_cnt + post_size)
            ]

            ForumPost.objects.bulk_create(new_post_list)

            print("done.")
        else:
            print("parameter user_size must > 0")
