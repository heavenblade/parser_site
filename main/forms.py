import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Grammar

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)

    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Your passowrd must contain at least 8 characters and 1 number'

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        help_texts = {
            'username': _(''),
            'email': _('Insert valid email'),
        }

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        valid_email = re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email)
        if (valid_email):
            return(email)
        else:
            raise forms.ValidationError("Insert a valid email")

    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data["email"]
        if (commit):
            user.save()
        return(user)


class MyGrammarInsertForm(forms.ModelForm):
    grammar_productions = forms.CharField(
        label = '',
        required = True,
        widget = forms.Textarea(
            attrs = {
                "id": "lr0_prod_text_area",
                "placeholder": "S->AB\nA->a\nB->#",
                "rows": 10,
                "cols": 20,
            }
        )
    )

    class Meta:
        model = Grammar
        fields = [
            'grammar_productions',
        ]

    def clean_grammar_productions(self, *args, **kwargs): ### Checks for valid grammar input
        grammar_prods = self.cleaned_data.get('grammar_productions')
        productions = grammar_prods.split('\n')
        valid_grammar = True
        for prod in productions:
            if not (prod[0].isupper()): ### Already checked if left hand side is non-terminal
                valid_grammar = False
                break
        if (valid_grammar):
            return(grammar_prods)
        else:
            raise forms.ValidationError("You inserted a non valid grammar")

    def save(self, commit = True):
        my_grammar = super(MyGrammarInsertForm, self).save(commit = False)
        my_grammar.grammar_productions = self.cleaned_data["grammar_productions"]
        my_grammar.grammar_terminal_symbols = self.cleaned_data["grammar_terminal_symbols"]
        my_grammar.grammar_nonTerminal_symbols = self.cleaned_data["grammar_nonTerminal_symbols"]
        my_grammar.grammar_used_parser = self.cleaned_data["grammar_used_parser"]
        my_grammar.grammar_parsing_table_entries = self.cleaned_data["grammar_parsing_table_entries"]
        my_grammar.grammar_user_submitter = self.cleaned_data["grammar_user_submitter"]
        my_grammar.grammar_timestamp = self.cleaned_data["grammar_timestamp"]
        if (commit):
            my_grammar.save()
        return(my_grammar)
