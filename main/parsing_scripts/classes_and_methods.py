from .ffc import isNonTerminal
import numpy
import sys

#------------------------------------------------------------------------------
class nonTerminal:
    name = ''
    first_l = []
    follow_l = []
    isStartSymbol = False

    def __init__ (self, non_terminal_name):
        self.name = non_terminal_name
        self.first_l = []
        self.follow_l = []
        self.isStartSymbol = False

    def add_first (self, element):
        self.first_l.append(element)

    def add_follow (self, element):
        self.follow_l.append(element)
#------------------------------------------------------------------------------
class lr0Item:
    production = []
    type = ""
    dot = 0
    isReduceItem = False

    def __init__ (self, production, type, dot, reduct):
        self.production = production
        self.type = type
        self.dot = dot
        self.isReduceItem = reduct

    def __eq__ (self, other):
        if (self.production == other.production and self.type == other.type and self.dot == other.dot and self.isReduceItem == other.isReduceItem):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.production, self.type, self.dot, self.isReduceItem))

def create_new_item (production, type, dot, reduct):
    new_state = lr0Item(production, type, dot, reduct)
    return new_state

def print_item(item):
    print(item.production, item.type, item.dot, item.isReduceItem)
#------------------------------------------------------------------------------
class lr0State:
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
#------------------------------------------------------------------------------
class transition:
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
    new_transition = transition(name, element, s_state, e_state)
    return new_transition
