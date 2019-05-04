from .utils import support_variables as sv
# function that returns True if a symbol is terminal and False otherwise
def isTerminal(element):
    isSymbol = False
    if element == "(" or element == ")" or element == "*" or element == "+" or element == "." or element == "-" or element == "[" or element == "]" or element == "<" or element == ">" or element == "=" or element == "^" or element == "{" or element == "}" or element == "|":
        isSymbol = True
    if element == element.upper() and not isSymbol:
        return False
    elif element == element.lower() or isSymbol:
        return True

# function that returns True if a symbol is non-terminal and False otherwise
def isNonTerminal(element):
    isSymbol = False
    if element == "(" or element == ")" or element == "*" or element == "+" or element == "." or element == "-" or element == "[" or element == "]" or element == "<" or element == ">" or element == "=" or element == "^" or element == "{" or element == "}" or element == "|":
        isSymbol = True
    if element == element.upper() and not isSymbol:
        return True
    elif element == element.lower() or isSymbol:
        return False

# function that returns the set of terminal symbols in a given grammar
def collect_terminal_symbols(grammar):
    terminal_names = []
    for production in grammar:
        for index in range(len(production[0])):
            if production[0][index] != '#' and index >= 3:
                if isTerminal(production[0][index]):
                    if production[0][index] not in terminal_names:
                        terminal_names.append(production[0][index])
    terminal_names.append("$")
    return terminal_names

# function that returns the set of non-terminal symbols in a given grammars
def collect_nonTerminal_symbols(grammar):
    non_terminal_names = []
    non_terminals = []
    for production in grammar:
        driver = production[0][0]
        if driver not in non_terminal_names:
            non_terminal_names.append(driver)
            non_terminals.append(nonTerminal(driver))
    non_terminals[0].isStartSymbol = True
    return non_terminal_names, non_terminals

# function that return the set of first symbols (+ epsilon) of a given non-terminal symbol
def compute_first(driver, production, my_non_terminals, p_prog):
    if driver.name == production[0][0]:
        #print("Analyzing '" + production[0] + "' in the computation of first(" + driver.name + ").")
        if isTerminal(production[0][p_prog]):
            if production[0][p_prog] not in driver.first_l:
                driver.add_first(production[0][p_prog])
                #print("Adding '" + production[0][p_prog] + "' to first(" + driver.name + ").")
            #else:
                #print("'" + production[0][p_prog] + "' already in first(" + driver.name + ").")
        elif production[0][p_prog] == '#' and p_prog == len(production[0])-1:
            if '#' not in driver.first_l:
                driver.add_first('#')
                #print("Adding epsilon to first(" + driver.name + ").")
        elif isNonTerminal(production[0][p_prog]):
            for element in my_non_terminals:
                if element.name == production[0][p_prog]:
                    nT = element
                    for first_nT in nT.first_l:
                        if first_nT != '#':
                            if first_nT not in driver.first_l:
                                driver.add_first(first_nT)
                                #print("Adding '" + first_nT + "' to first(" + driver.name + ").")
                            #else:
                                #print("'" + first_nT + "' already in first(" + driver.name + ").")
                        else:
                            if p_prog == len(production[0])-1:
                                if "#" not in driver.first_l:
                                    driver.add_first("#")
                                    #print("Adding epsilon to first(" + driver.name + ").")
                            else:
                                if p_prog < len(production[0])-1:
                                    #print("Calling again")
                                    compute_first(driver, production, my_non_terminals, p_prog+1)

# function that returns the set of follow symbols (+ $) of a given non-terminal symbol
def compute_follow(nT, production, my_non_terminals, p_prog):
    if nT.isStartSymbol:
        if '$' not in nT.follow_l:
            nT.add_follow('$')
    #print("Analyzing the production '" + production[0] + "' in the computation of follow(" + nT.name + ")..")
    if production[0][-1] == nT.name:
        for non_T in my_non_terminals:
            if production[0][0] == non_T.name:
                for follow_d in non_T.follow_l:
                    if follow_d not in nT.follow_l:
                        nT.follow_l.append(follow_d)
                        #print("Adding '" + follow_d + "' to follow(" + production[0][-1] + ") due to rule 1.")
    if nT.name == production[0][p_prog]:
        stopped = False
        if len(production[0]) > 4 and p_prog < len(production[0])-1:
            if isNonTerminal(production[0][p_prog]):
                if isTerminal(production[0][p_prog+1]):
                    if production[0][p_prog+1] not in nT.follow_l:
                        nT.add_follow(production[0][p_prog+1])
                        #print("Adding '" + production[0][p_prog+1] + "' to follow(" + nT.name + ") due to rule 2.")
                        compute_follow(nT, production, my_non_terminals, p_prog+1)
                else:
                    while (p_prog < len(production[0])-1 and not stopped):
                        if isTerminal(production[0][p_prog+1]):
                            if production[0][p_prog+1] not in nT.follow_l:
                                nT.add_follow(production[0][p_prog+1])
                            stopped = True
                        else:
                            for non_T_ahead in my_non_terminals:
                                if non_T_ahead.name == production[0][p_prog+1]:
                                    if "#" in non_T_ahead.first_l:
                                        for first_to_add in non_T_ahead.first_l:
                                            if first_to_add != "#":
                                                if first_to_add not in nT.follow_l:
                                                    nT.add_follow(first_to_add)
                                                    #print("Adding '" + first_to_add + "' to follow(" + nT.name + ") due to rule 3.1")
                                        if p_prog+1 == len(production[0])-1:
                                            for driver_non_T in my_non_terminals:
                                                if driver_non_T.name == production[0][0]:
                                                    for follow_driver in driver_non_T.follow_l:
                                                        if follow_driver not in nT.follow_l:
                                                            nT.add_follow(follow_driver)
                                                            #print("Adding '" + follow_driver + "' to follow(" + nT.name + ") due to rule 4")
                                            stopped = True
                                        if p_prog+2 <= len(production[0])-1:
                                            p_prog += 1
                                    else:
                                        for first_to_add in non_T_ahead.first_l:
                                            if first_to_add not in nT.follow_l:
                                                nT.add_follow(first_to_add)
                                                #print("Adding '" + first_to_add + "' to follow(" + nT.name + ") due to rule 3.2")
                                        stopped = True
                                        break
        else:
            if isNonTerminal(production[0][p_prog]):
                for element in my_non_terminals:
                    if element.name == production[0][-1]:
                        for driver in my_non_terminals:
                            if driver.name == production[0][0]:
                                for follow_d in driver.follow_l:
                                    if follow_d not in element.follow_l:
                                        element.add_follow(follow_d)
                                        #print("Adding '" + follow_d + "' to follow(" + production[0][-1] + ") due to rule 1.")
    else:
        if p_prog < len(production[0])-1:
            compute_follow(nT, production, my_non_terminals, p_prog+1)
#------------------------------------------------------------------------------
class Transition:
    name = 0
    element = ''
    starting_state = 0
    ending_state = 0

    def __init__(self, transition_count, elem, s_state, e_state):
        self.name = transition_count
        self.element = elem
        self.starting_state = s_state
        self.ending_state = e_state

    def create_new_transition(name, element, s_state, e_state):
        new_transition = Transition(name, element, s_state, e_state)
        return new_transition
#------------------------------------------------------------------------------
class RecursiveEquation:
    name = ""
    symbol_list = []
    solved = False

    def __init__(self, name):
        self.name = name
        self.symbol_list = []
        self.solved = False

    def __str__(self):
        return str(self.name)

    def create_new_rec_equation():
        rec_eq_name = "x"+str(sv.rec_equations_counter)
        new_equation = RecursiveEquation(rec_eq_name)
        sv.rec_equations_counter += 1
        return new_equation
#------------------------------------------------------------------------------
class nonTerminal:
    name = ''
    first_l = []
    follow_l = []
    isStartSymbol = False

    def __init__(self, non_terminal_name):
        self.name = non_terminal_name
        self.first_l = []
        self.follow_l = []
        self.isStartSymbol = False

    def add_first(self, element):
        self.first_l.append(element)

    def add_follow(self, element):
        self.follow_l.append(element)
#------------------------------------------------------------------------------
class lr0Item:
    production = []
    type = ""
    dot = 0
    isReduceItem = False
    set_of_rec_equations = []

    def __init__(self, production, type, dot, reduct):
        self.production = production
        self.type = type
        self.dot = dot
        self.isReduceItem = reduct
        self.set_of_rec_equations = []

    def __eq__(self, other):
        if self.production == other.production and self.type == other.type and self.dot == other.dot and self.isReduceItem == other.isReduceItem:
            return True
        else:
            return False

    def __str__(self):
        return self.production

    def __hash__(self):
        return hash((self.production, self.type, self.dot, self.isReduceItem))

    def create_new_item(production, type, dot, reduct):
        new_item = lr0Item(production, type, dot, reduct)
        return new_item
#------------------------------------------------------------------------------
class lr0State:
    name = 0
    item_l = []
    isInitialState = False

    def __init__(self, state_count):
        self.name = state_count
        self.item_l = []
        self.isInitialState = False

    def create_new_state(name):
        new_state = lr0State(name)
        return new_state

    def check_kernel_equality(new_kernel, state_n):
        state_n_ker = []
        for item in state_n.item_l:
            if item.type == "Kernel":
                state_n_ker.append(item)
        if set(new_kernel) == set(state_n_ker):
            return True
        else:
            return False

    def apply_closure(state, my_item, grammar):
        if my_item.isReduceItem == "Not-Reduce":
            if isNonTerminal(my_item.production[my_item.dot]):
                for production in grammar:
                    if production[0][0] == my_item.production[my_item.dot]:
                        if production[0][3] == "#":
                            new_item = lr0Item.create_new_item(production[0], "Closure", 3, "Reduce")
                        else:
                            new_item = lr0Item.create_new_item(production[0], "Closure", 3, "Not-Reduce")
                        if new_item not in state.item_l:
                            state.item_l.append(new_item)
                            if isNonTerminal(new_item.production[new_item.dot]):
                                lr0State.apply_closure(state, new_item, grammar)

    def apply_closure_lalr_version(state, my_item, recursion, grammar, non_terminals, rec_equations):
        if my_item.isReduceItem == "Not-Reduce":
            if isNonTerminal(my_item.production[my_item.dot]):
                for production in grammar:
                    if production[0][0] == my_item.production[my_item.dot]:
                        temp_lookAhead_l = []
                        if my_item.dot == len(my_item.production)-1:
                            for element in my_item.set_of_rec_equations:
                                if element not in temp_lookAhead_l:
                                    temp_lookAhead_l.append(element)
                        else:
                            p_prog = my_item.dot
                            stopped = False
                            while p_prog+1 <= len(my_item.production)-1 and not stopped:
                                if isTerminal(my_item.production[p_prog+1]):
                                    if my_item.production[p_prog+1] not in temp_lookAhead_l:
                                        temp_lookAhead_l.append(my_item.production[p_prog+1])
                                        stopped = True
                                else:
                                    for nT in non_terminals:
                                        if nT.name == my_item.production[p_prog+1]:
                                            for first_nT in nT.first_l:
                                                if first_nT != "#":
                                                    if first_nT not in temp_lookAhead_l:
                                                        temp_lookAhead_l.append(first_nT)
                                                else:
                                                    if p_prog+1 == len(my_item.production)-1:
                                                        for item_clos_rec_eq in my_item.set_of_rec_equations:
                                                            if item_clos_rec_eq not in temp_lookAhead_l:
                                                                temp_lookAhead_l.append(item_clos_rec_eq)
                                p_prog += 1
                        if production[0][3] == "#":
                            new_temp_item = lr0Item.create_new_item(production[0], "Closure", 3, "Reduce")
                            temp_type = "Reduce"
                        else:
                            new_temp_item = lr0Item.create_new_item(production[0], "Closure", 3, "Not-Reduce")
                            temp_type = "Not-Reduce"
                        found = False
                        for item_for_la_merge in state.item_l:
                            tmp_item = lr0Item.create_new_item(item_for_la_merge.production, item_for_la_merge.type, item_for_la_merge.dot, item_for_la_merge.isReduceItem)
                            if tmp_item == new_temp_item:
                                for la_to_merge in temp_lookAhead_l:
                                    if la_to_merge not in item_for_la_merge.set_of_rec_equations[0].symbol_list:
                                        item_for_la_merge.set_of_rec_equations[0].symbol_list.append(la_to_merge)
                                found = True
                        if not found:
                            new_item = lr0Item.create_new_item(production[0], "Closure", 3, temp_type)
                            new_item_rec_eq = RecursiveEquation.create_new_rec_equation()
                            for symb_to_add in temp_lookAhead_l:
                                if symb_to_add not in new_item_rec_eq.symbol_list:
                                    new_item_rec_eq.symbol_list.append(symb_to_add)
                            new_item.set_of_rec_equations.append(new_item_rec_eq)
                            rec_equations.append(new_item_rec_eq)
                            if new_item not in state.item_l:
                                state.item_l.append(new_item)
                                #print("Adding " + new_item.production + " to state " + str(state.name))
                                if recursion < 2:
                                    if isNonTerminal(new_item.production[new_item.dot]):
                                        #print("recurring for " + new_item.production, recursion)
                                        lr0State.apply_closure_lalr_version(state, new_item, recursion+1, grammar, non_terminals, rec_equations)
#------------------------------------------------------------------------------
class lr1Item:
    production = []
    lookAhead = []
    type = ""
    dot = 0
    isReduceItem = False

    def __init__(self, production, LA, type, dot, reduct):
        self.production = production
        self.lookAhead = LA
        self.type = type
        self.dot = dot
        self.isReduceItem = reduct

    def __eq__(self, other):
        equal = False
        lookaheads = []
        if self.production == other.production and self.type == other.type and self.dot == other.dot and self.isReduceItem == other.isReduceItem:
            for element in self.lookAhead:
                if element not in lookaheads:
                    lookaheads.append(element)
            for element in other.lookAhead:
                if element not in lookaheads:
                    lookaheads.append(element)
            for LA in lookaheads:
                if LA in self.lookAhead:
                    if LA in other.lookAhead:
                        equal = True
                    else:
                        equal = False
                        break
                else:
                    equal = False
                    break
        else:
            equal = False
        if equal:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.production, self.type, self.dot, self.isReduceItem))

    def create_new_item(production, LA, type, dot, reduct):
        new_item = lr1Item(production, LA, type, dot, reduct)
        return new_item

    def set_lookaheads(self, lookahead_l):
        self.lookAhead = lookahead_l
#------------------------------------------------------------------------------
class lr1State:
    name = 0
    item_l = []
    isInitialState = False

    def __init__(self, state_count):
        self.name = state_count
        self.item_l = []
        self.isInitialState = False

    def add_item(self, item):
        self.item_l.append(item)

    def create_new_state(name):
        new_state = lr1State(name)
        return new_state

    def check_kernel_equality(new_kernel, state_n):
        state_n_ker = []
        for item in state_n.item_l:
            if item.type == "Kernel":
                state_n_ker.append(item)
        if set(new_kernel) == set(state_n_ker):
            return True
        else:
            return False

    def apply_closure(state, my_item, recursion, grammar, non_terminals):
        if my_item.isReduceItem == "Not-Reduce":
            if isNonTerminal(my_item.production[my_item.dot]):
                for production in grammar:
                    if production[0][0] == my_item.production[my_item.dot]:
                        temp_lookAhead_l = []
                        if my_item.dot == len(my_item.production)-1:
                            for element in my_item.lookAhead:
                                temp_lookAhead_l.append(element)
                        else:
                            p_prog = my_item.dot
                            stopped = False
                            while (p_prog+1 <= len(my_item.production)-1 and not stopped):
                                if isTerminal(my_item.production[p_prog+1]):
                                    if my_item.production[p_prog+1] not in temp_lookAhead_l:
                                        temp_lookAhead_l.append(my_item.production[p_prog+1])
                                        stopped = True
                                else:
                                    for nT in non_terminals:
                                        if nT.name == my_item.production[p_prog+1]:
                                            for first_nT in nT.first_l:
                                                if first_nT != "#":
                                                    if first_nT not in temp_lookAhead_l:
                                                        temp_lookAhead_l.append(first_nT)
                                                else:
                                                    if p_prog+1 == len(my_item.production)-1:
                                                        for item_clos_LA in my_item.lookAhead:
                                                            if item_clos_LA not in temp_lookAhead_l:
                                                                temp_lookAhead_l.append(item_clos_LA)
                                p_prog += 1
                        temp_type = ""
                        if production[0][3] == "#":
                            new_temp_item = lr0Item.create_new_item(production[0], "Closure", 3, "Reduce")
                            temp_type = "Reduce"
                        else:
                            new_temp_item = lr0Item.create_new_item(production[0], "Closure", 3, "Not-Reduce")
                            temp_type = "Not-Reduce"
                        found = False
                        for item_for_la_merge in state.item_l:
                            temp_item = lr0Item.create_new_item(item_for_la_merge.production, item_for_la_merge.dot, item_for_la_merge.type, item_for_la_merge.isReduceItem)
                            if temp_item == new_temp_item:
                                for la_to_merge in temp_lookAhead_l:
                                    if la_to_merge not in item_for_la_merge.lookAhead:
                                        item_for_la_merge.lookAhead.append(la_to_merge)
                                found = True
                        if not found:
                            new_item = lr1Item.create_new_item(production[0], temp_lookAhead_l, "Closure", 3, temp_type)
                            if new_item not in state.item_l:
                                state.item_l.append(new_item)
                                #print("Adding " + new_item.production + " to state " + str(state.name))
                                if recursion < 2:
                                    if isNonTerminal(new_item.production[new_item.dot]):
                                        #print("recurring for " + new_item.production, recursion)
                                        lr1State.apply_closure(state, new_item, recursion+1, grammar, non_terminals)
