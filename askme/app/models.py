from django.db import models
from django.contrib.auth.models import User


class ModelManager(models.Manager):
    def get_hot_questions(self):
        return self.order_by('-rating')
    

    def get_useful_answers(self):
        return self.annotate(num_likes=models.Count('likes')).order_by('-num_likes')
    

    def get_question_with_special_tag(self, tag_name):
        return self.filter(tags__name=tag_name)
    

    def get_popular_tags(self):
        return self.annotate(num_questions=models.Count('questions')).order_by('-num_questions')
    

    def get_five_best_members(self):
        return self.annotate(total_likes=models.Sum('answer__likes__id')).order_by('-total_likes')[:5]
    

class Profile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='upload/', default='upload/User.png')
    objects = ModelManager()


    def __str__(self):
        return self.profile.username


class Tag(models.Model):
    name = models.CharField(max_length=25)
    objects = ModelManager()


    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
    rating = models.ManyToManyField(Profile, related_name='temporary_rating')
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='questions')
    objects = ModelManager()


    def __str__(self):
        return self.name


class Answer(models.Model):
    text = models.CharField(max_length=255)
    likes = models.ManyToManyField(Profile, through='Like', related_name='liked_answers')
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = ModelManager()

    
    def __str__(self):
        return f'Answer to question: "{self.question.name}"'
    

class Like(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
