import numpy
import sys
# from .ffc import isTerminal, isNonTerminal

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

    def __init__(self, production, type, dot, reduct):
        self.production = production
        self.type = type
        self.dot = dot
        self.isReduceItem = reduct

    def __eq__(self, other):
        if (self.production == other.production and self.type == other.type and self.dot == other.dot and self.isReduceItem == other.isReduceItem):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.production, self.type, self.dot, self.isReduceItem))

    def print_item(self):
        print(self.production, self.type, self.dot, self.isReduceItem)

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

    def add_item(self, item):
        self.item_l.append(item)

    def create_new_state(name):
        new_state = lr0State(name)
        return new_state

    def check_kernel_equality(new_kernel, state_n):
        state_n_ker = []
        for item in state_n.item_l:
            if (item.type == "Kernel"):
                state_n_ker.append(item)
        if (set(new_kernel) == set(state_n_ker)):
            return True
        else:
            return False

    def apply_closure(state, my_item):
        if (my_item.isReduceItem == "Not-Reduce"):
            if (isNonTerminal(my_item.production[my_item.dot])):
                for production in grammar:
                    if (production[0][0] == my_item.production[my_item.dot]):
                        if (production[0][3] == "#"):
                            new_item = create_new_item(production[0], "Closure", 3, "Reduce")
                        else:
                            new_item = create_new_item(production[0], "Closure", 3, "Not-Reduce")
                        if (new_item not in state.item_l):
                            state.add_item(new_item)
                            if (isNonTerminal(new_item.production[new_item.dot])):
                                apply_closure(state, new_item)

    def print_state(self):
        for item in self.item_l:
            item.print_item()
#------------------------------------------------------------------------------
class lr1Item:
    production = []
    lookAhead = []
    dot = 0
    type = ""
    isReduceItem = False

    def __init__ (self, production, LA, dot, type, reduct):
        self.production = production
        self.lookAhead = LA
        self.dot = dot
        self.type = type
        self.isReduceItem = reduct

    def __eq__ (self, other):
        equal = False
        lookaheads = []
        if (self.production == other.production and self.dot == other.dot and self.type == other.type and self.isReduceItem == other.isReduceItem):
            for element in self.lookAhead:
                if (element not in lookaheads):
                    lookaheads.append(element)
            for element in other.lookAhead:
                if (element not in lookaheads):
                    lookaheads.append(element)
            for LA in lookaheads:
                if (LA in self.lookAhead):
                    if (LA in other.lookAhead):
                        equal = True
                    else:
                        equal = False
                        break
                else:
                    equal = False
                    break
        else:
            equal = False
        if (equal):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.production, self.dot, self.type, self.isReduceItem))

    def create_new_lr1_item (production, LA, dot, type, reduct):
        new_item = lr1Item(production, LA, dot, type, reduct)
        return new_item

    def print_item(item):
        print(item.production, item.lookAhead, item.dot, item.type, item.isReduceItem)
#------------------------------------------------------------------------------
class lr1State:
    name = 0
    item_l = []
    isInitialState = False

    def __init__ (self, state_count):
        self.name = state_count
        self.item_l = []
        self.isInitialState = False

    def add_item (self, item):
        self.item_l.append(item)

    def create_new_state (name):
        new_state = lr1State(name)
        return new_state

    def check_kernel_equality(new_kernel, state_n):
        state_n_ker = []
        for item in state_n.item_l:
            if (item.type == "Kernel"):
                state_n_ker.append(item)
        if (set(new_kernel) == set(state_n_ker)):
            return True
        else:
            return False

    def apply_closure(state, my_item, recursion):
        if (my_item.isReduceItem == "Not-Reduce"):
            if (ffc.isNonTerminal(my_item.production[my_item.dot])):
                for production in grammar:
                    if (production[0][0] == my_item.production[my_item.dot]):
                        temp_lookAhead_l = []
                        if (my_item.dot == len(my_item.production)-1):
                            for element in my_item.lookAhead:
                                temp_lookAhead_l.append(element)
                        else:
                            p_prog = my_item.dot
                            stopped = False
                            while (p_prog+1 <= len(my_item.production)-1 and not stopped):
                                if (ffc.isTerminal(my_item.production[p_prog+1])):
                                    if (my_item.production[p_prog+1] not in temp_lookAhead_l):
                                        temp_lookAhead_l.append(my_item.production[p_prog+1])
                                        stopped = True
                                else:
                                    for nT in non_terminals:
                                        if (nT.name == my_item.production[p_prog+1]):
                                            for first_nT in nT.first_l:
                                                if (first_nT != "#"):
                                                    if (first_nT not in temp_lookAhead_l):
                                                        temp_lookAhead_l.append(first_nT)
                                                else:
                                                    if (p_prog+1 == len(my_item.production)-1):
                                                        for item_clos_LA in my_item.lookAhead:
                                                            if (item_clos_LA not in temp_lookAhead_l):
                                                                temp_lookAhead_l.append(item_clos_LA)
                                p_prog += 1
                        temp_type = ""
                        if (production[0][3] == "#"):
                            new_temp_item = create_new_lr0_item(production[0], 3, "Closure", "Reduce")
                            temp_type = "Reduce"
                        else:
                            new_temp_item = create_new_lr0_item(production[0], 3, "Closure", "Not-Reduce")
                            temp_type = "Not-Reduce"
                        found = False
                        for item_for_la_merge in state.item_l:
                            temp_item = create_new_lr0_item(item_for_la_merge.production, item_for_la_merge.dot, item_for_la_merge.type, item_for_la_merge.isReduceItem)
                            if (temp_item == new_temp_item):
                                for la_to_merge in temp_lookAhead_l:
                                    if (la_to_merge not in item_for_la_merge.lookAhead):
                                        item_for_la_merge.lookAhead.append(la_to_merge)
                                found = True
                        if (not found):
                            new_item = create_new_lr1_item(production[0], temp_lookAhead_l, 3, "Closure", temp_type)
                            if (new_item not in state.item_l):
                                state.item_l.append(new_item)
                                #print("Adding " + new_item.production + " to state " + str(state.name))
                                if (recursion < 2):
                                    if (ffc.isNonTerminal(new_item.production[new_item.dot])):
                                        #print("recurring for " + new_item.production, recursion)
                                        apply_closure(state, new_item, recursion+1)
#------------------------------------------------------------------------------
class lr0Transition:
    name = 0
    element = ''
    starting_state = 0
    ending_state = 0

    def __init__ (self, transition_count, elem, s_state, e_state):
        self.name = transition_count
        self.element = elem
        self.starting_state = s_state
        self.ending_state = e_state

    def create_new_transition (name, element, s_state, e_state):
        new_transition = lr0Transition(name, element, s_state, e_state)
        return new_transition
