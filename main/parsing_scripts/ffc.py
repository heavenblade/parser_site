# This is a utility file that contains functions to verify if an element
# is a terminal or a non-terminal, the two main functions that compute first
# and follow of a given non-terminal and the final check to verify if the table
# contains any multiply defined entry.
# Check readme.md in order to see input format of the grammar and eventual
# output format.
#
# Author: Matteo Amatori

from .classes_and_methods import nonTerminal

# function that returns True if a symbol is terminal and False otherwise
def isTerminal(element):
    isSymbol = False
    if (element == "(" or element == ")" or element == "*" or element == "+" or element == "." or element == "-" or element == "[" or element == "]" or element == "<" or element == ">" or element == "=" or element == "^" or element == "{" or element == "}" or element == "|"):
        isSymbol = True
    if (element == element.upper() and not isSymbol):
        return False
    elif (element == element.lower() or isSymbol):
        return True

# function that returns True if a symbol is non-terminal and False otherwise
def isNonTerminal(element):
    isSymbol = False
    if (element == "(" or element == ")" or element == "*" or element == "+" or element == "." or element == "-" or element == "[" or element == "]" or element == "<" or element == ">" or element == "=" or element == "^" or element == "{" or element == "}" or element == "|"):
        isSymbol = True
    if (element == element.upper() and not isSymbol):
        return True
    elif (element == element.lower() or isSymbol):
        return False

# function that returns the set of terminal symbols in a given grammar
def collect_terminal_symbols(grammar):
    terminal_names = []
    for production in grammar:
        for index in range(len(production[0])):
            if (production[0][index] != '#' and index >= 3):
                if (isTerminal(production[0][index])):
                    if (production[0][index] not in terminal_names):
                        terminal_names.append(production[0][index])
    terminal_names.append("$")
    return terminal_names

# function that returns the set of non-terminal symbols in a given grammars
def collect_nonTerminal_symbols(grammar):
    non_terminal_names = []
    non_terminals = []
    for index in range(len(grammar)):
        driver = grammar[index][0][0]
        if driver not in non_terminal_names:
            non_terminal_names.append(driver)
            non_terminals.append(nonTerminal(driver))
    return non_terminal_names, non_terminals

# function that return the set of first symbols (+ epsilon) of a given non-terminal symbol
def compute_first(driver, production, my_non_terminals, p_prog):
    if (driver.name == production[0][0]):
        #print("Analyzing '" + production[0] + "' in the computation of first(" + driver.name + ").")
        if (isTerminal(production[0][p_prog])):
            if production[0][p_prog] not in driver.first_l:
                driver.add_first(production[0][p_prog])
                #print("Adding '" + production[0][p_prog] + "' to first(" + driver.name + ").")
            #else:
                #print("'" + production[0][p_prog] + "' already in first(" + driver.name + ").")
        elif (production[0][p_prog] == '#' and p_prog == len(production[0])-1):
            if '#' not in driver.first_l:
                driver.add_first('#')
                #print("Adding epsilon to first(" + driver.name + ").")
        elif (isNonTerminal(production[0][p_prog])):
            for element in my_non_terminals:
                if element.name == production[0][p_prog]:
                    nT = element
                    for first_nT in nT.first_l:
                        if (first_nT != '#'):
                            if first_nT not in driver.first_l:
                                driver.add_first(first_nT)
                                #print("Adding '" + first_nT + "' to first(" + driver.name + ").")
                            #else:
                                #print("'" + first_nT + "' already in first(" + driver.name + ").")
                        else:
                            if (p_prog == len(production[0])-1):
                                if "#" not in driver.first_l:
                                    driver.add_first("#")
                                    #print("Adding epsilon to first(" + driver.name + ").")
                            else:
                                if (p_prog < len(production[0])-1):
                                    #print("Calling again")
                                    compute_first(driver, production, my_non_terminals, p_prog+1)

# function that returns the set of follow symbols (+ $) of a given non-terminal symbol
def compute_follow(nT, production, my_non_terminals, p_prog):
    if (nT.isStartSymbol):
        if ('$' not in nT.follow_l):
            nT.add_follow('$')
    #print("Analyzing the production '" + production[0] + "' in the computation of follow(" + nT.name + ")..")
    if (production[0][-1] == nT.name):
        for non_T in my_non_terminals:
            if (production[0][0] == non_T.name):
                for follow_d in non_T.follow_l:
                    if (follow_d not in nT.follow_l):
                        nT.follow_l.append(follow_d)
                        #print("Adding '" + follow_d + "' to follow(" + production[0][-1] + ") due to rule 1.")
    if (nT.name == production[0][p_prog]):
        stopped = False
        if (len(production[0]) > 4 and p_prog < len(production[0])-1):
            if (isNonTerminal(production[0][p_prog])):
                if (isTerminal(production[0][p_prog+1])):
                    if (production[0][p_prog+1] not in nT.follow_l):
                        nT.add_follow(production[0][p_prog+1])
                        #print("Adding '" + production[0][p_prog+1] + "' to follow(" + nT.name + ") due to rule 2.")
                        compute_follow(nT, production, my_non_terminals, p_prog+1)
                else:
                    while (p_prog < len(production[0])-1 and not stopped):
                        if (isTerminal(production[0][p_prog+1])):
                            if (production[0][p_prog+1] not in nT.follow_l):
                                nT.add_follow(production[0][p_prog+1])
                            stopped = True
                        else:
                            for non_T_ahead in my_non_terminals:
                                if (non_T_ahead.name == production[0][p_prog+1]):
                                    if ("#" in non_T_ahead.first_l):
                                        for first_to_add in non_T_ahead.first_l:
                                            if (first_to_add != "#"):
                                                if (first_to_add not in nT.follow_l):
                                                    nT.add_follow(first_to_add)
                                                    #print("Adding '" + first_to_add + "' to follow(" + nT.name + ") due to rule 3.1")
                                        if (p_prog+1 == len(production[0])-1):
                                            for driver_non_T in my_non_terminals:
                                                if (driver_non_T.name == production[0][0]):
                                                    for follow_driver in driver_non_T.follow_l:
                                                        if (follow_driver not in nT.follow_l):
                                                            nT.add_follow(follow_driver)
                                                            #print("Adding '" + follow_driver + "' to follow(" + nT.name + ") due to rule 4")
                                            stopped = True
                                        if (p_prog+2 <= len(production[0])-1):
                                            p_prog += 1
                                    else:
                                        for first_to_add in non_T_ahead.first_l:
                                            if (first_to_add not in nT.follow_l):
                                                nT.add_follow(first_to_add)
                                                #print("Adding '" + first_to_add + "' to follow(" + nT.name + ") due to rule 3.2")
                                        stopped = True
                                        break
        else:
            if (isNonTerminal(production[0][p_prog])):
                for element in my_non_terminals:
                    if (element.name == production[0][-1]):
                        for driver in my_non_terminals:
                            if (driver.name == production[0][0]):
                                for follow_d in driver.follow_l:
                                    if follow_d not in element.follow_l:
                                        element.add_follow(follow_d)
                                        #print("Adding '" + follow_d + "' to follow(" + production[0][-1] + ") due to rule 1.")
    else:
        if (p_prog < len(production[0])-1):
            compute_follow(nT, production, my_non_terminals, p_prog+1)
