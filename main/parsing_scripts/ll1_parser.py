from .classes_and_methods import isNonTerminal, isTerminal, nonTerminal, collect_nonTerminal_symbols, collect_terminal_symbols, compute_first, compute_follow


def compute_ll1_parsing(grammar):
    # return declaration
    table_entries = []
    non_terminal_names = []
    non_terminals = []
    terminals = []
    first_set = {}
    follow_set = {}

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

    # table creation
    header = []
    header.append('Non terminals')
    for element in terminals:
        if element not in header:
            header.append(element)

    table = [["" for x in range(len(header))] for y in range(len(non_terminal_names))]

    for idx_row, element in enumerate(non_terminal_names, 0):
        for idx_col in range(len(header)):
            if (idx_col == 0):
                table[idx_row][idx_col] = element
            else:
                table[idx_row][idx_col] = []

    # table computation
    for production in grammar:
        symbols_checked = []
        derives_eps_check = 0
        p_prog = 3
        if (production[0][p_prog] == '#'):
            for element in non_terminals:
                if (element.name == production[0][0]):
                    nT = element
                    for follow_nT in nT.follow_l:
                        driver_index = 0
                        terminal_index = 0
                        for idx, element_1 in enumerate(non_terminal_names, 0):
                            if (element_1 == production[0][0]):
                                driver_index = idx
                        for idx, element_2 in enumerate(terminals, 0):
                            if (element_2 == follow_nT):
                                terminal_index = idx
                        table[driver_index][terminal_index+1].append(production[0])
        elif (isTerminal(production[0][p_prog])):
            driver_index = 0
            terminal_index = 0
            for idx, element in enumerate(non_terminal_names, 0):
                if (element == production[0][0]):
                    driver_index = idx
            for idx, element in enumerate(terminals, 0):
                if (element == production[0][p_prog]):
                    terminal_index = idx
            table[driver_index][terminal_index+1].append(production[0])
        elif (isNonTerminal(production[0][p_prog])):
            stopped = False
            while (p_prog <= len(production[0])-1 and not stopped):
                for nT in non_terminals:
                    if (nT.name == production[0][p_prog]):
                        if ("#" in nT.first_l):
                            #print(nT.name, derives_eps_check, derives_eps_check+1)
                            derives_eps_check += 1
                            for first_nT in nT.first_l:
                                if (first_nT != '#'):
                                    driver_index = 0
                                    terminal_index = 0
                                    for idx, element_1 in enumerate(non_terminal_names, 0):
                                        if (element_1 == production[0][0]):
                                            driver_index = idx
                                    for idx, element_2 in enumerate(terminals, 0):
                                        if (element_2 == first_nT):
                                            terminal_index = idx
                                    #print("Adding " + production[0] + " to [" + str(driver_index) + "," + str(terminal_index) + "] - 1 watching " + production[0][p_prog])
                                    if (first_nT not in symbols_checked):
                                        table[driver_index][terminal_index+1].append(production[0])
                                        symbols_checked.append(first_nT)
                            if (isTerminal(production[0][p_prog+1])):
                                driver_index = 0
                                terminal_index = 0
                                for idx, element in enumerate(non_terminal_names, 0):
                                    if (element == production[0][0]):
                                        driver_index = idx
                                for idx, element in enumerate(terminals, 0):
                                    if (element == production[0][p_prog+1]):
                                        terminal_index = idx
                                #print("Adding " + production[0] + " to [" + str(driver_index) + "," + str(terminal_index) + "] - 2 watching " + production[0][p_prog])
                                if (production[0][p_prog+1] not in symbols_checked):
                                    table[driver_index][terminal_index+1].append(production[0])
                                    symbols_checked.append(production[0][p_prog+1])
                                stopped = True
                            elif (isNonTerminal(production[0][p_prog+1])):
                                for nT_ahead in non_terminals:
                                    if (nT_ahead.name == production[0][p_prog+1]):
                                        if ("#" in nT_ahead.first_l):
                                            #print(nT_ahead.name, derives_eps_check, derives_eps_check+1)
                                            derives_eps_check += 1
                                            for first_nT_ahead in nT_ahead.first_l:
                                                if (first_nT_ahead != '#'):
                                                    driver_index = 0
                                                    terminal_index = 0
                                                    for idx, element_1 in enumerate(non_terminal_names, 0):
                                                        if (element_1 == production[0][0]):
                                                            driver_index = idx
                                                    for idx, element_2 in enumerate(terminals, 0):
                                                        if (element_2 == first_nT_ahead):
                                                            terminal_index = idx
                                                    #print("Adding " + production[0] + " to [" + str(driver_index) + "," + str(terminal_index) + "] - 3 watching " + production[0][p_prog])
                                                    if (first_nT_ahead not in symbols_checked):
                                                        table[driver_index][terminal_index+1].append(production[0])
                                                        symbols_checked.append(first_nT_ahead)
                                            if (p_prog+1 == len(production[0])-1):
                                                stopped = True
                                                if (derives_eps_check + 3 == len(production[0])):
                                                    for driver_non_T in non_terminals:
                                                        if (production[0][0] == driver_non_T.name):
                                                            for follow_driver_non_T in driver_non_T.follow_l:
                                                                driver_index = 0
                                                                terminal_index = 0
                                                                for idx, element_1 in enumerate(non_terminal_names, 0):
                                                                    if (element_1 == production[0][0]):
                                                                        driver_index = idx
                                                                for idx, element_2 in enumerate(terminals, 0):
                                                                    if (element_2 == follow_driver_non_T):
                                                                        terminal_index = idx
                                                                #print("Adding " + production[0] + " to [" + str(driver_index) + "," + str(terminal_index) + "] - 4 watching " + production[0][p_prog])
                                                                table[driver_index][terminal_index+1].append(production[0])
                                            if (p_prog+2 <= len(production[0])-1):
                                                p_prog += 1
                                        else:
                                            for first_nT_ahead in nT_ahead.first_l:
                                                driver_index = 0
                                                terminal_index = 0
                                                for idx, element_1 in enumerate(non_terminal_names, 0):
                                                    if (element_1 == production[0][0]):
                                                        driver_index = idx
                                                for idx, element_2 in enumerate(terminals, 0):
                                                    if (element_2 == first_nT_ahead):
                                                        terminal_index = idx
                                                #print("Adding " + production[0] + " to [" + str(driver_index) + "," + str(terminal_index) + "] - 5 watching " + production[0][p_prog])
                                                if (first_nT_ahead not in symbols_checked):
                                                    table[driver_index][terminal_index+1].append(production[0])
                                                    symbols_checked.append(first_nT_ahead)
                                            stopped = True
                        else:
                            for first_nT in nT.first_l:
                                driver_index = 0
                                terminal_index = 0
                                for idx, element_1 in enumerate(non_terminal_names, 0):
                                    if (element_1 == production[0][0]):
                                        driver_index = idx
                                for idx, element_2 in enumerate(terminals, 0):
                                    if (element_2 == first_nT):
                                        terminal_index = idx
                                #print("Adding " + production[0] + " to [" + str(driver_index) + "," + str(terminal_index) + "] - 6 watching " + production[0][p_prog])
                                table[driver_index][terminal_index+1].append(production[0])
                            stopped = True

    return table, terminals, non_terminal_names, non_terminals, first_set, follow_set
