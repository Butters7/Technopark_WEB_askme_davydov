from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, LikedAnswers, LikedQuestions
from faker import Faker
import random

def fill_bd(ratio):
    faker = Faker('en_US')

    for i in range(ratio):
        user = User.objects.create_user(username=f'user{i}')
        user.set_password(f'django{i}')
        user.save()

        profile = Profile.objects.create(profile=user)

    
    for i in range(ratio):
        tag = Tag.objects.create(name=f'tag{i}')


    for i in range(ratio * 10):
        title = f'Question{i}'
        text = faker.text(max_nb_chars=1000)
        author = random.choice(Profile.objects.all())
        tags = []

        for i in range(3):
            tag = random.choice(Tag.objects.all())
            if tag not in tags:
                tags.append(tag)

        question = Question.objects.create(name=title, text=text, user_profile=author)
        question.tags.set(tags)
        question.save()

    
    for i in range(ratio * 10):
        for question in Question.objects.all():
            text = faker.text(max_nb_chars=1000)
            responder = Profile.objects.order_by('?').first()
            answer = Answer.objects.create(text=text, question=question, user_profile=responder)

    
    for i in range(ratio * 100):
        question = Question.objects.all()[i % 100001]
        user_profile = Profile.objects.all()[i % 10002]

        try:
            like = LikedQuestions.objects.create(question=question, user_profile=user_profile)
        except ValueError:
            pass
        except IntegrityError:
            pass


    for i in range(ratio * 100):
        answer = Answer.objects.all().reverse()[i % 1479012]
        user_profile = Profile.objects.all()[i % 10002]

        try:
            rating = LikedAnswers.objects.create(answer=answer, user_profile=user_profile)
        except ValueError:
            pass
        except IntegrityError:
            pass



class Command(BaseCommand):
    help = 'Filling data base'


    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('START TO FILLING DB'))
        ratio = options.get('ratio')
        fill_bd(ratio=ratio[0])
        self.stdout.write(self.style.SUCCESS('SUCCESFULLY FILLED DB'))
