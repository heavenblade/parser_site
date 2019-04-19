from .classes_and_methods import isNonTerminal, isTerminal, collect_nonTerminal_symbols, collect_terminal_symbols, compute_first, compute_follow, lr0Item, lr1Item, lr0State, Transition, RecursiveEquation

def compute_lalr1_parsing(grammar):
    # return declaration
    table_entries = []
    non_terminal_names = []
    non_terminals = []
    terminals = []
    first_set = {}
    follow_set = {}
    lr0_states = []
    transitions = []
    rec_equations = []
    state_counter = 0
    transition_counter = 0
    rec_equations_counter = 0

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

    for symbol in non_terminals:
        first_set[symbol.name] = symbol.first_l
        follow_set[symbol.name] = symbol.follow_l

    # creation of augmented grammar
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
    s_item = lr0Item.create_new_item(a_grammar[0], 3, "Kernel", "Not-Reduce")
    initial_lookahead, rec_equations_counter = RecursiveEquation.create_new_rec_equation(rec_equations_counter)
    initial_lookahead.symbol_list.append("$")
    s_item.add_rec_equation(initial_lookahead)
    rec_equations.append(initial_lookahead)
    initial_state.add_item(s_item)
    lr0State.apply_closure_lalr_version(initial_state, s_item, 0, grammar, non_terminals, rec_equations_counter)
    lr0_states.append(initial_state)

    # rest of automaton computation
    for state in lr0_states:
        for i in range(3): # temporary solution to recursive closure applications
            for clos_item in state.item_l:
                lr0State.apply_closure_lalr_version(state, clos_item, 0, grammar, non_terminals, rec_equations_counter)
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
                        new_item = lr0Item.create_new_item(item.production, item.dot+1, "Kernel", "Reduce" if item.dot+1 == len(item.production) else "Not-Reduce")
                        for rec_eq in item.set_of_rec_equations:
                            new_item.add_rec_equation(rec_eq)
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
                    lr0State.apply_closure_lalr_version(new_state, new_state_item, 0, grammar, non_terminals, rec_equations_counter)
                new_transition = Transition.create_new_transition(transition_counter, element, state.name, new_state.name)
                transition_counter += 1
                if new_transition not in transitions:
                    transitions.append(new_transition)
            else:
                new_transition = Transition.create_new_transition(transition_counter, element, state.name, destination_state)
                transition_counter += 1
                if new_transition not in transitions:
                    transitions.append(new_transition)
                for arrival_state in lr0_states:
                    if arrival_state.name == destination_state:
                        for item_dep_state in state.item_l:
                            for item_arr_state in arrival_state.item_l:
                                if item_dep_state == item_arr_state:
                                    for rec_eq_dep_item in item_dep_state.set_of_rec_equations:
                                        if rec_eq_dep_item not in item_arr_state.set_of_rec_equations:
                                            item_arr_state.set_of_rec_equations.append(rec_eq_dep_item)
                                            #print("Adding " + rec_eq_dep_item + " from " + item_dep_state.production + " to " + item_arr_state.production)

    # recursive equations solving
    finished_solving = False
    while (not finished_solving):
        for rec_eq in rec_equations:
            while(not rec_eq.solved):
                for element in rec_eq.symbol_list:
                    if not isinstance(element, str):
                        rec_eq.symbol_list.remove(element)
                        #print("Removing " + element.name + " from " + rec_eq.name + " and adding ", element.symbol_list)
                        for symbol in element.symbol_list:
                            if symbol not in rec_eq.symbol_list:
                                rec_eq.symbol_list.append(symbol)
                if not all(isinstance(elem, str) for elem in rec_eq.symbol_list):
                    rec_eq.solved = False
                else:
                    rec_eq.solved = True
                    #print("Solved: " + rec_eq.name + " =", rec_eq.symbol_list, "")
        if all(rec_eq.solved for rec_eq in rec_equations):
            finished_solving = True
        else:
            finished_solving = False
    '''
    print(rec_equations)
    for rec_eq in rec_equations:
        print(rec_eq.name + " =", rec_eq.symbol_list)
    print("LALR(1)-states:")
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
            print(prod_to_print + ", " + element.type + ", " + element.isReduceItem + ",", element.set_of_rec_equations[0].symbol_list)
    print("LALR(1)-transitions:")
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
            if "Q->" not in item.production:
                new_entry = ""
                if item.isReduceItem == "Reduce":
                    for idx1, production in enumerate(grammar):
                        if item.production == production[0]:
                            new_entry = "R" + str(idx1+1)
                    for idx2, element in enumerate(header):
                        for rec_eq_symbol in item.set_of_rec_equations[0].symbol_list:
                            if element == rec_eq_symbol:
                                if len(new_entry) > 0:
                                    table[state.name][idx2].append(new_entry)

    return table, terminals, non_terminal_names, non_terminals, first_set, follow_set
