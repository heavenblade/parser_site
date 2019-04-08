from .classes_and_methods import nonTerminal, lr0Item
from .ffc import collect_nonTerminal_symbols, collect_terminal_symbols, compute_first


def compute_lr0_parsing(grammar):
    # return declaration
    table_entries = []
    non_terminal_names = []
    non_terminals = []
    terminals = []

    # collecting non-terminal symbols
    non_terminal_names, non_terminals = collect_nonTerminal_symbols(grammar)
    non_terminals[0].isStartSymbol = True
    # collecting terminal symbols
    terminals = collect_terminal_symbols(grammar)

    # first computation
    for i in range(0, 2):
        for element in reversed(non_terminals):
            for row in grammar:
                compute_first(element, row, non_terminals, 3)


    return table_entries, terminals, non_terminal_names, non_terminals
