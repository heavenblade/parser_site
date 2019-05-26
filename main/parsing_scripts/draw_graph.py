from graphviz import Digraph

def drawGraph(states, transitions, type):
    dot = Digraph(comment = "Automaton", format = "png")
    dot.graph_attr['rankdir'] = 'LR'
    dot.graph_attr['fontname'] = 'Helvetica'
    dot.graph_attr['fontsize'] = '12'

    if type == '0':
        # cycle on states for the nodes
        for state in states:
            items = []
            for item in state.item_l:
                prod_to_print = ""
                prod_to_print += item.production[:3]
                if item.isReduceItem == "Reduce":
                    if item.production[3] == "#":
                        prod_to_print += "."
                    else:
                        prod_to_print += item.production[3:]
                        prod_to_print += "."
                else:
                    idx = 3
                    dot_added = False
                    while idx < len(item.production):
                        if idx != item.dot:
                            prod_to_print += item.production[idx]
                            idx += 1
                        elif idx == item.dot and not dot_added:
                            prod_to_print += "."
                            prod_to_print += item.production[idx]
                            dot_added = True
                        else:
                            idx += 1
                items.append(prod_to_print)
            dot.node(str(state.name), '\n'.join(items))
    elif type == '1':
            # cycle on states for the nodes
            for state in states:
                items = []
                for item in state.item_l:
                    prod_to_print = ""
                    prod_to_print += item.production[:3]
                    if item.isReduceItem == "Reduce":
                        if item.production[3] == "#":
                            prod_to_print += "."
                        else:
                            prod_to_print += item.production[3:]
                            prod_to_print += "."
                    else:
                        idx = 3
                        dot_added = False
                        while idx < len(item.production):
                            if idx != item.dot:
                                prod_to_print += item.production[idx]
                                idx += 1
                            elif idx == item.dot and not dot_added:
                                prod_to_print += "."
                                prod_to_print += item.production[idx]
                                dot_added = True
                            else:
                                idx += 1
                    lookaheads = ', [' + ','.join(item.lookAhead) + ']'
                    prod_to_print += lookaheads
                    items.append(prod_to_print)
                dot.node(str(state.name), '\n'.join(items))

    # cycle on transitions for arrows
    for transition in transitions:
        dot.edge(str(transition.starting_state), str(transition.ending_state), transition.element)

    return(dot)
