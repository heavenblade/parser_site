from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/MAmatori/Downloads/graphviz-2.38/release/bin'

# grammar tested:
# S->Aa
# A->d

# classes
class State():
    name = ""
    items = []

    def __init__(self, name, items):
        self.name = name
        self.items = items

class Transition():
    start = ""
    end = ""
    label = ""

    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

# States composition
s0 = State('0', ['Q->.S', 'S->.Aa', 'S->.d'])
s1 = State('1', ['Q->S.'])
s2 = State('2', ['S->A.a'])
s3 = State('3', ['S->d.'])
s4 = State('4', ['S->Aa.'])

states = []
states.append(s0)
states.append(s1)
states.append(s2)
states.append(s3)
states.append(s4)

# Transition composition
t0 = Transition('0', '1', 'S')
t1 = Transition('0', '2', 'A')
t2 = Transition('0', '3', 'd')
t3 = Transition('2', '4', 'a')

transitions = []
transitions.append(t0)
transitions.append(t1)
transitions.append(t2)
transitions.append(t3)

# graph creation
dot = Digraph(comment = "Automaton", format = "png")
dot.graph_attr['rankdir'] = 'LR'

# cycle on states for the nodes
for element in states:
    dot.node(element.name, '\n'.join(element.items))

# cycle on transitions for arrows
for element in transitions:
    dot.edge(element.start, element.end, element.label)

# output
print(dot.source)
dot.render('C:\\Users\\MAmatori\\Downloads\\graphs\\test_automaton.gv', view = True)




#
#
#
#
