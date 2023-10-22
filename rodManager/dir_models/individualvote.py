from django.db import models

class IndividualVote(models.Model):
    voter = models.ForeignKey('Account', on_delete=models.CASCADE)
    vote = models.ForeignKey('Vote', on_delete=models.CASCADE)
    option = models.IntegerField()
    date = models.DateField()