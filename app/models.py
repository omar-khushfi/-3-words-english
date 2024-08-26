from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Word(models.Model):
    arabic=models.TextField(max_length=50)
    english=models.TextField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Unknown_word(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    word=models.ForeignKey(Word,on_delete=models.CASCADE)
    