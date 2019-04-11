from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms.models import model_to_dict


# Create your models here.
class Grammar(models.Model):
    grammar_productions = models.TextField()
    grammar_terminal_symbols = models.TextField()
    grammar_nonTerminal_symbols = models.TextField()
    grammar_first_set = models.TextField()
    grammar_follow_set = models.TextField()
    grammar_used_parser = models.CharField(max_length = 20)
    grammar_parsing_table_entries = models.TextField()
    grammar_user_submitter = models.ForeignKey(User, on_delete = models.CASCADE)
    grammar_timestamp = models.DateTimeField('Date submitted', default = timezone.now())

    def __str__(self):
        return(self.grammar_productions)

    def first_set_as_dict(self):
        print(model_to_dict(self)['grammar_first_set'])
        return(model_to_dict(self)['grammar_first_set'])

    def follow_set_as_dict(self):
        return(self.grammar_follow_set.split(','))
