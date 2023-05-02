from django.db import models

# Create your models here.

class Words(models.Model):

    word = models.CharField(verbose_name="Word", max_length=100)
    translation = models.CharField(verbose_name="Translation", max_length=30)
    pinyin = models.CharField(verbose_name="Pinyin", max_length=30)

    def __str__(self):
        return self.word + " - " + self.translation + " - " + self.pinyin 