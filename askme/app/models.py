from django.db import models
from django.contrib.auth.models import User


class ModelManager(models.Manager):
    def get_news_question(self):
        return self.order_by('-id')


    def get_hot_questions(self):
        return self.annotate(num_likes=models.Count('likes')).order_by('-num_likes')
    

    def get_question_with_special_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-id')
    

    def get_popular_tags(self):
        return self.annotate(num_questions=models.Count('questions')).order_by('-num_questions')[:4]
    

    def get_five_best_members(self):
        return self.annotate(total_likes=models.Count('liked_answers')).order_by('-total_likes')[:5]
    

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
    text = models.TextField()
    likes = models.ManyToManyField(Profile, through='LikedQuestions', related_name='liked_questions', blank=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='questions')
    objects = ModelManager()   


    def __str__(self): 
        return self.name


class Answer(models.Model):
    text = models.TextField()
    likes = models.ManyToManyField(Profile, through='LikedAnswers', related_name='liked_answers', blank=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = ModelManager()

    
    def __str__(self):
        return f'{self.user_profile.profile.username} answer to question: "{self.question.name}"'
    

class LikedAnswers(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['answer', 'user_profile'], name='unique_answer_likes')
        ]


    def __str__(self):
        return f'{self.user_profile.profile.username} liked answer "{self.answer.pk}"'


class LikedQuestions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'user_profile'], name='unique_question_likes')
        ]
        

    def __str__(self):
        return f'{self.user_profile.profile.username} rate question "{self.question.name}"'
