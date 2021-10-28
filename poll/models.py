from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    question = models.TextField()
    options = models.JSONField(default=list)
    options_count = models.JSONField(default=list)

    def __str__(self):
        return self.question

    def snippet(self):
        return self.question[:80]

class Vote(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    chosen = models.CharField(blank=True,null=True,max_length=200)

    def __str__(self):
        return self.chosen
