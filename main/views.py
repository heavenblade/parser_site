from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Grammar
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import MyRegistrationForm, MyGrammarInsertForm
from django.utils import timezone

# Views
def homepage(request):
    return(render(request = request, template_name = "main/parsers_home.html"))

def register(request):
    if (request.method == "POST"):
        reg_form = MyRegistrationForm(data = request.POST)
        if (reg_form.is_valid()):
            user = reg_form.save()
            username = reg_form.cleaned_data.get('username')
            messages.success(request, f"Welcome {username}")
            login(request, user)
            return(redirect("main:homepage"))
        else:
            for msg in reg_form.error_messages:
                messages.error(request, f"{msg}:{reg_form.error_messages[msg]}")
    reg_form = MyRegistrationForm
    return(render(request = request, template_name = "main/register.html", context = {"reg_form": reg_form}))

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return(redirect("main:homepage"))

def login_request(request):
    if (request.method == "POST"):
        log_form = AuthenticationForm(request, data = request.POST)
        if (log_form.is_valid()):
            usr = log_form.cleaned_data.get('username')
            pwd = log_form.cleaned_data.get('password')
            user = authenticate(username = usr, password = pwd)
            if (user is not None):
                login(request, user)
                messages.success(request, f"You are now logged in as {usr}")
                return(redirect("main:homepage"))
            else:
                messages.error(request, f"Invalid username or password")
    log_form = AuthenticationForm()
    return(render(request = request, template_name = "main/login.html", context = {"form": log_form}))

def user_page(request):
    grammars_to_show = []
    for grammar_entry in Grammar.objects.all():
        if (grammar_entry.grammar_user_submitter == request.user):
            grammars_to_show.append(grammar_entry)
    return(render(request = request, template_name = "main/user_page.html", context = {"grammars": grammars_to_show}))

def about_page(request):
    return(render(request = request, template_name = "main/about_page.html"))

def lr0_parser(request):
    lr0_form = MyGrammarInsertForm()
    grammar = None
    if (request.method == "POST"):
        lr0_form = MyGrammarInsertForm(request.POST)
        if (lr0_form.is_valid()):
            lr0_form.cleaned_data['grammar_used_parser'] = 'LR(0)'
            lr0_form.cleaned_data['grammar_parsing_table_entries'] = ''
            lr0_form.cleaned_data['grammar_user_submitter'] = request.user
            lr0_form.cleaned_data['grammar_timestamp'] = timezone.now()
            if not (Grammar.objects.filter(grammar_productions = lr0_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lr0').exists()):
                grammar = lr0_form.save()
            else:
                print("Grammar already exists") ### Return that grammar which is already saved in database (maybe with the same method as the check above)
        else:
            messages.error(request, f"Please insert a grammar")
    return(render(request = request, template_name = "main/lr0_parser_page.html", context = {"form": lr0_form, "grammar": grammar}))

def dyn_grammar_parsing(request, grammar_id):
    grammar = Grammar.objects.get(id = grammar_id)
    return(render(request = request, template_name = "main/lr0_grammar_parsing.html", context = {"grammar": grammar}))

def slr0_parser(request):
    return(render(request = request, template_name = "main/slr0_parser_page.html"))

def lr1_parser(request):
    return(render(request = request, template_name = "main/lr1_parser_page.html"))

def lalr1_parser(request):
    return(render(request = request, template_name = "main/lalr1_parser_page.html"))

def ll1_parser(request):
    return(render(request = request, template_name = "main/ll1_parser_page.html"))
