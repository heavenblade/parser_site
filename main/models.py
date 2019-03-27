from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Grammar(models.Model):
    grammar_productions = models.TextField()
    grammar_used_parser = models.CharField(max_length = 20)
    grammar_parsing_table_entries = models.TextField()
    grammar_user_submitter = models.ForeignKey(User, on_delete = models.CASCADE)
    grammar_timestamp = models.DateTimeField('Date submitted', default = timezone.now())

    def __str__(self):
        return(self.grammar_productions)
