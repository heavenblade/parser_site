from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms.models import model_to_dict
import ast


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

    def productions_as_list(self):
        return(self.grammar_productions.split('\r\n'))

    def get_first_set_as_list(self):
        return(ast.literal_eval(self.grammar_first_set))

    def get_follow_set_as_list(self):
        return(ast.literal_eval(self.grammar_follow_set))

    def get_terminals_as_list(self):
        return(ast.literal_eval(self.grammar_terminal_symbols))

    def get_nonTerminals_as_list(self):
        return(ast.literal_eval(self.grammar_nonTerminal_symbols))

    def get_grammar_productions_as_list(self):
        return(ast.literal_eval(self.grammar_parsing_table_entries))

    def get_joined_table_entries(self):
        if len(self) > 1:
            return(" / ".join(self))
        else:
            return(self)
