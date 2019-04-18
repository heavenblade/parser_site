from .classes_and_methods import isNonTerminal, isTerminal, collect_nonTerminal_symbols, collect_terminal_symbols, compute_first, compute_follow, lr0State, lr0Item, lr0Transition


def compute_slr0_parsing(grammar):
    # variabls and return declaration
    non_terminal_names = []
    non_terminals = []
    terminals = []
    first_set = {}
    follow_set = {}
    lr0_states = []
    transitions = []
    state_counter = 0
    transition_counter = 0

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

    # follow computation
    for i in range(0, 1):
        for element in non_terminals:
            for row in grammar:
                compute_follow(element, row, non_terminals, 3)

    # storing first and follow for return
    for symbol in non_terminals:
        first_set[symbol.name] = symbol.first_l
        follow_set[symbol.name] = symbol.follow_l

    # augumented grammar
    a_grammar = []
    prev_starting_symb = ''
    for element in non_terminals:
        if element.isStartSymbol:
            prev_starting_symb = element.name
    starting_prod = "Q->" + prev_starting_symb
    a_grammar.append(starting_prod)
    for prod in grammar:
        a_grammar.append(prod[0])

    # starting state
    initial_state = lr0State.create_new_state(state_counter)
    state_counter += 1
    initial_state.isInitialState = True
    s_item = lr0Item.create_new_item(a_grammar[0], "Kernel", 3, "Not-Reduce")
    initial_state.add_item(s_item)
    lr0State.apply_closure(initial_state, s_item, grammar)
    lr0_states.append(initial_state)

    # rest of automaton computation
    for state in lr0_states:
        for i in range(3): # temporary solution to recursive closure applications
            for clos_item in state.item_l:
                lr0State.apply_closure(state, clos_item, grammar)
        new_symb_transitions = []
        for item in state.item_l:
            if item.isReduceItem == "Not-Reduce":
                if item.production[item.dot] not in new_symb_transitions:
                    new_symb_transitions.append(item.production[item.dot])
        for element in new_symb_transitions:
            require_new_state = False
            destination_state = 0
            new_state_items = []
            for item in state.item_l:
                if item.isReduceItem != "Reduce":
                    if item.production[item.dot] == element:
                        new_item = lr0Item.create_new_item(item.production, "Kernel", item.dot+1, "Reduce" if (item.dot+1 == len(item.production)) else "Not-Reduce")
                        new_state_items.append(new_item)
            for state_n in lr0_states:
                if lr0State.check_kernel_equality(new_state_items, state_n):
                    require_new_state = False
                    destination_state = state_n.name
                    break
                else:
                    require_new_state = True
            if require_new_state:
                new_state = lr0State.create_new_state(state_counter)
                state_counter += 1
                lr0_states.append(new_state)
                for new_state_item in new_state_items:
                    if new_state_item not in new_state.item_l:
                        new_state.add_item(new_state_item)
                    lr0State.apply_closure(new_state, new_state_item, grammar)
                new_transition = lr0Transition.create_new_transition(transition_counter, element, state.name, new_state.name)
                transition_counter += 1
                if new_transition not in transitions:
                    transitions.append(new_transition)
            else:
                new_transition = lr0Transition.create_new_transition(transition_counter, element, state.name, destination_state)
                transition_counter += 1
                if new_transition not in transitions:
                    transitions.append(new_transition)
    '''
    print("LR(0)-states:")
    for state in lr0_states:
        print("State " + str(state.name) + ":")
        for element in state.item_l:
            prod_to_print = ""
            prod_to_print += element.production[:3]
            if (element.isReduceItem == "Reduce"):
                if (element.production[3] == "#"):
                    prod_to_print += "."
                else:
                    prod_to_print += element.production[3:]
                    prod_to_print += "."
            else:
                idx = 3
                dot_added = False
                while (idx < len(element.production)):
                    if (idx != element.dot):
                        prod_to_print += element.production[idx]
                        idx += 1
                    elif (idx == element.dot and not dot_added):
                        prod_to_print += "."
                        prod_to_print += element.production[idx]
                        dot_added = True
                    else:
                        idx += 1
            print(prod_to_print + ",", element.type + ", " + element.isReduceItem)
    print("LR(0)-transitions:")
    for transition in transitions:
        print(transition.name, transition.element, transition.starting_state, transition.ending_state)
    '''
    # table creation
    header = []
    header.append('States')
    for element in terminals:
        if element not in header:
            header.append(element)
    for element in non_terminal_names:
        if element not in header:
            header.append(element)

    table = [["" for x in range(len(header))] for y in range(state_counter)]

    for idx_row in range(state_counter):
        for idx_col in range(len(header)):
            if idx_col == 0:
                table[idx_row][idx_col] = idx_row
            else:
                table[idx_row][idx_col] = []

    for idx, element in enumerate(header):
        if element == "$":
            table[1][idx].append("Accept")
    for transition in transitions:
        new_entry = ""
        if isNonTerminal(transition.element):
            new_entry = "Goto " + str(transition.ending_state)
            for idx, element in enumerate(header):
                if element == transition.element:
                    table[transition.starting_state][idx].append(new_entry)
        elif isTerminal(transition.element):
            new_entry = "S" + str(transition.ending_state)
            for idx, element in enumerate(header):
                if element == transition.element:
                    table[transition.starting_state][idx].append(new_entry)
    for state in lr0_states:
        for item in state.item_l:
            found = False
            if "Q->" not in item.production:
                new_entry = ""
                if item.isReduceItem == "Reduce":
                    for non_terminal in non_terminals:
                        if non_terminal.name == item.production[0]:
                            nT = non_terminal
                            found = True
                    for idx1, production in enumerate(grammar):
                        if item.production == production[0]:
                            new_entry = "R" + str(idx1+1)
                    for idx2, element in enumerate(header):
                        if found:
                            for follow_nT in nT.follow_l:
                                if follow_nT == element:
                                    if len(new_entry) > 0:
                                        table[state.name][idx2].append(new_entry)

    return table, terminals, non_terminal_names, non_terminals, first_set, follow_set
