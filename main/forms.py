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

    def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data["email"]
        if (commit):
            user.save()
        return(user)

class MyGrammarInsertForm(forms.ModelForm):
    grammar = forms.CharField(required = True)

    def __init__(self, user, *args, **kwargs):
        super(MyGrammarInsertForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)
        self.fields['grammar'].label = ""

    class Meta:
        model = Grammar

        fields = [
            'grammar',
        ]

        widgets = {
            'grammar': forms.Textarea(),
        }

    def save(self, commit = True):
        grammar = super(MyGrammarInsertForm, self).save(commit = False)
        grammar.grammar_productions = self.cleaned_data["grammar"]
        grammar.grammar_used_parser = "lr0"
        grammar.grammar_parsing_table_entries = "WIP"
        grammar.grammar_user_submitter = user
        if (commit):
            grammar.save()
        return(grammar)
