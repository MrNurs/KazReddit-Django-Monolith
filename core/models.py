from django.db import models
from django.contrib.auth.models import User

class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        words = self.name.split()
        self.name = ''.join(word.capitalize() for word in words)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class Post(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(default="null")
    def __str__(self):
        return self.title
    author = models.CharField(max_length=100)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100, default="<UNK>")
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text} - {self.author}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('user', 'comment')