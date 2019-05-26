from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Grammar
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import MyRegistrationForm, MyGrammarInsertForm
from django.utils import timezone
from .parsing_scripts.classes_and_methods import collect_terminal_symbols
from .parsing_scripts.lr0_parser import compute_lr0_parsing
from .parsing_scripts.slr0_parser import compute_slr0_parsing
from .parsing_scripts.lr1_parser import compute_lr1_parsing
from .parsing_scripts.lalr1_parser import compute_lalr1_parsing
from .parsing_scripts.ll1_parser import compute_ll1_parsing
import ast
import os

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
            lr0_form.cleaned_data['grammar_used_parser'] = 'lr0'
            lr0_form.cleaned_data['grammar_parsing_table_entries'] = ''
            if request.user.is_authenticated:
                lr0_form.cleaned_data['grammar_user_submitter'] = request.user
            else:
                lr0_form.cleaned_data['grammar_user_submitter'] = None
            lr0_form.cleaned_data['grammar_timestamp'] = timezone.now()
            if not (Grammar.objects.filter(grammar_productions = lr0_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lr0').exists()):
                processed_grammar = []
                for production in lr0_form.cleaned_data['grammar_productions'].split('\r\n'):
                    processed_grammar.append([production])
                table, terminals, nonTerminals, non_terminals_obj, first_set, follow_set, graph = compute_lr0_parsing(processed_grammar)
                lr0_form.cleaned_data['grammar_terminal_symbols'] = terminals
                lr0_form.cleaned_data['grammar_nonTerminal_symbols'] = nonTerminals
                lr0_form.cleaned_data['grammar_first_set'] = first_set
                lr0_form.cleaned_data['grammar_follow_set'] = follow_set
                lr0_form.cleaned_data['grammar_parsing_table_entries'] = table
                grammar = lr0_form.save()
                os.environ["PATH"] += os.pathsep + 'C:/Users/MAmatori/Downloads/graphviz-2.38/release/bin'
                graph.render('C:/Users/MAmatori/Documents/repo_parsers/parser_site/main/static/img/graphs/graph_' + str(grammar.id), view = False, format = "png")
            else:
                grammar = Grammar.objects.get(grammar_productions = lr0_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lr0')
            return(redirect('/lr0-parser/parsing-grammar-' + str(grammar.id)))
        else:
            messages.error(request, f"Please insert a grammar")
    return(render(request = request, template_name = "main/lr0_parser_page.html", context = {"form": lr0_form, "grammar": grammar}))

def slr0_parser(request):
    slr0_form = MyGrammarInsertForm()
    grammar = None
    if (request.method == "POST"):
        slr0_form = MyGrammarInsertForm(request.POST)
        if (slr0_form.is_valid()):
            slr0_form.cleaned_data['grammar_used_parser'] = 'slr0'
            slr0_form.cleaned_data['grammar_parsing_table_entries'] = ''
            if request.user.is_authenticated:
                slr0_form.cleaned_data['grammar_user_submitter'] = request.user
            else:
                slr0_form.cleaned_data['grammar_user_submitter'] = None
            slr0_form.cleaned_data['grammar_timestamp'] = timezone.now()
            if not (Grammar.objects.filter(grammar_productions = slr0_form.cleaned_data['grammar_productions'], grammar_used_parser = 'slr0').exists()):
                processed_grammar = []
                for production in slr0_form.cleaned_data['grammar_productions'].split('\r\n'):
                    processed_grammar.append([production])
                table, terminals, nonTerminals, non_terminals_obj, first_set, follow_set, graph = compute_slr0_parsing(processed_grammar)
                slr0_form.cleaned_data['grammar_terminal_symbols'] = terminals
                slr0_form.cleaned_data['grammar_nonTerminal_symbols'] = nonTerminals
                slr0_form.cleaned_data['grammar_first_set'] = first_set
                slr0_form.cleaned_data['grammar_follow_set'] = follow_set
                slr0_form.cleaned_data['grammar_parsing_table_entries'] = table
                grammar = slr0_form.save()
                os.environ["PATH"] += os.pathsep + 'C:/Users/MAmatori/Downloads/graphviz-2.38/release/bin'
                graph.render('C:/Users/MAmatori/Documents/repo_parsers/parser_site/main/static/img/graphs/graph_' + str(grammar.id), view = False, format = "png")
            else:
                grammar = Grammar.objects.get(grammar_productions = slr0_form.cleaned_data['grammar_productions'], grammar_used_parser = 'slr0')
            return(redirect('/slr0-parser/parsing-grammar-' + str(grammar.id)))
        else:
            messages.error(request, f"Please insert a grammar")
    return(render(request = request, template_name = "main/slr0_parser_page.html", context = {"form": slr0_form, "grammar": grammar}))

def lr1_parser(request):
    lr1_form = MyGrammarInsertForm()
    grammar = None
    if (request.method == "POST"):
        lr1_form = MyGrammarInsertForm(request.POST)
        if (lr1_form.is_valid()):
            lr1_form.cleaned_data['grammar_used_parser'] = 'lr1'
            lr1_form.cleaned_data['grammar_parsing_table_entries'] = ''
            if request.user.is_authenticated:
                lr1_form.cleaned_data['grammar_user_submitter'] = request.user
            else:
                lr1_form.cleaned_data['grammar_user_submitter'] = None
            lr1_form.cleaned_data['grammar_timestamp'] = timezone.now()
            if not (Grammar.objects.filter(grammar_productions = lr1_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lr1').exists()):
                processed_grammar = []
                for production in lr1_form.cleaned_data['grammar_productions'].split('\r\n'):
                    processed_grammar.append([production])
                table, terminals, nonTerminals, non_terminals_obj, first_set, follow_set, graph = compute_lr1_parsing(processed_grammar)
                lr1_form.cleaned_data['grammar_terminal_symbols'] = terminals
                lr1_form.cleaned_data['grammar_nonTerminal_symbols'] = nonTerminals
                lr1_form.cleaned_data['grammar_first_set'] = first_set
                lr1_form.cleaned_data['grammar_follow_set'] = follow_set
                lr1_form.cleaned_data['grammar_parsing_table_entries'] = table
                grammar = lr1_form.save()
                os.environ["PATH"] += os.pathsep + 'C:/Users/MAmatori/Downloads/graphviz-2.38/release/bin'
                graph.render('C:/Users/MAmatori/Documents/repo_parsers/parser_site/main/static/img/graphs/graph_' + str(grammar.id), view = False, format = "png")
            else:
                grammar = Grammar.objects.get(grammar_productions = lr1_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lr1')
            return(redirect('/lr1-parser/parsing-grammar-' + str(grammar.id)))
        else:
            messages.error(request, f"Please insert a grammar")
    return(render(request = request, template_name = "main/lr1_parser_page.html", context = {"form": lr1_form, "grammar": grammar}))

def lalr1_parser(request):
    lalr1_form = MyGrammarInsertForm()
    grammar = None
    if (request.method == "POST"):
        lalr1_form = MyGrammarInsertForm(request.POST)
        if (lalr1_form.is_valid()):
            lalr1_form.cleaned_data['grammar_used_parser'] = 'lalr1'
            lalr1_form.cleaned_data['grammar_parsing_table_entries'] = ''
            if request.user.is_authenticated:
                lalr1_form.cleaned_data['grammar_user_submitter'] = request.user
            else:
                lalr1_form.cleaned_data['grammar_user_submitter'] = None
            lalr1_form.cleaned_data['grammar_timestamp'] = timezone.now()
            if not (Grammar.objects.filter(grammar_productions = lalr1_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lalr1').exists()):
                processed_grammar = []
                for production in lalr1_form.cleaned_data['grammar_productions'].split('\r\n'):
                    processed_grammar.append([production])
                table, terminals, nonTerminals, non_terminals_obj, first_set, follow_set = compute_lalr1_parsing(processed_grammar)
                lalr1_form.cleaned_data['grammar_terminal_symbols'] = terminals
                lalr1_form.cleaned_data['grammar_nonTerminal_symbols'] = nonTerminals
                lalr1_form.cleaned_data['grammar_first_set'] = first_set
                lalr1_form.cleaned_data['grammar_follow_set'] = follow_set
                lalr1_form.cleaned_data['grammar_parsing_table_entries'] = table
                grammar = lalr1_form.save()
                # os.environ["PATH"] += os.pathsep + 'C:/Users/MAmatori/Downloads/graphviz-2.38/release/bin'
                # graph.render('C:/Users/MAmatori/Documents/repo_parsers/parser_site/main/static/img/graphs/graph_' + str(grammar.id), view = False, format = "png")
            else:
                grammar = Grammar.objects.get(grammar_productions = lalr1_form.cleaned_data['grammar_productions'], grammar_used_parser = 'lalr1')
            return(redirect('/lalr1-parser/parsing-grammar-' + str(grammar.id)))
        else:
            messages.error(request, f"Please insert a grammar")
    return(render(request = request, template_name = "main/lalr1_parser_page.html", context = {"form": lalr1_form, "grammar": grammar}))

def ll1_parser(request):
    ll1_form = MyGrammarInsertForm()
    grammar = None
    if (request.method == "POST"):
        ll1_form = MyGrammarInsertForm(request.POST)
        if (ll1_form.is_valid()):
            ll1_form.cleaned_data['grammar_used_parser'] = 'll1'
            ll1_form.cleaned_data['grammar_parsing_table_entries'] = ''
            if request.user.is_authenticated:
                ll1_form.cleaned_data['grammar_user_submitter'] = request.user
            else:
                ll1_form.cleaned_data['grammar_user_submitter'] = None
            ll1_form.cleaned_data['grammar_timestamp'] = timezone.now()
            if not (Grammar.objects.filter(grammar_productions = ll1_form.cleaned_data['grammar_productions'], grammar_used_parser = 'll1').exists()):
                processed_grammar = []
                for production in ll1_form.cleaned_data['grammar_productions'].split('\r\n'):
                    processed_grammar.append([production])
                table, terminals, nonTerminals, non_terminals_obj, first_set, follow_set = compute_ll1_parsing(processed_grammar)
                ll1_form.cleaned_data['grammar_terminal_symbols'] = terminals
                ll1_form.cleaned_data['grammar_nonTerminal_symbols'] = nonTerminals
                ll1_form.cleaned_data['grammar_first_set'] = first_set
                ll1_form.cleaned_data['grammar_follow_set'] = follow_set
                ll1_form.cleaned_data['grammar_parsing_table_entries'] = table
                grammar = ll1_form.save()
            else:
                grammar = Grammar.objects.get(grammar_productions = ll1_form.cleaned_data['grammar_productions'], grammar_used_parser = 'll1')
            return(redirect('/ll1-parser/parsing-grammar-' + str(grammar.id)))
        else:
            messages.error(request, f"Please insert a grammar")
    return(render(request = request, template_name = "main/ll1_parser_page.html", context = {"form": ll1_form, "grammar": grammar}))

def dyn_grammar_bu_parsing(request, grammar_id):
    grammar = Grammar.objects.get(id = grammar_id)
    first_follow_obj = zip(ast.literal_eval(grammar.grammar_first_set).items(), ast.literal_eval(grammar.grammar_follow_set).items())
    return(render(request = request, template_name = "main/grammar_bu_parsing.html", context = {"grammar": grammar, "ff_obj": first_follow_obj}))

def dyn_grammar_td_parsing(request, grammar_id):
    grammar = Grammar.objects.get(id = grammar_id)
    first_follow_obj = zip(ast.literal_eval(grammar.grammar_first_set).items(), ast.literal_eval(grammar.grammar_follow_set).items())
    return(render(request = request, template_name = "main/grammar_td_parsing.html", context = {"grammar": grammar, "ff_obj": first_follow_obj}))
