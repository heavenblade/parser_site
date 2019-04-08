from .classes_and_methods import nonTerminal, lr0Item
from .ffc import collect_nonTerminal_symbols, collect_terminal_symbols


def compute_lr0_parsing(grammar):
    # return declaration
    table_entries = []
    non_terminal_names = []
    non_terminals = []
    terminals = []
    first = []
    follow = []

    # collecting non-terminal symbols
    non_termoinal_names, non_terminals = collect_nonTerminal_symbols(grammar)
    # collecting terminal symbols
    terminals = collect_terminal_symbols(grammar)


    return table_entries, terminals, non_terminal_names, first, follow
