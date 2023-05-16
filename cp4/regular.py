import nfa

def singleton(w):
    """Returns a NFA recognizing the language {w}.

    (It's not a regular operation so it technically doesn't belong in
    this module.)
    """
    
    m = nfa.NFA()
    m.set_start(0)
    for i in range(len(w)):
        m.add_transition(nfa.Transition(i, w[i], i+1))
    m.add_accept(len(w))
    return m

def copy_into(m1, m2, offset=0):
    """Helper function that copies states and transitions from m1 into m2,
    renumbering the states and possibly adding an offset. Does *not*
    change start or accept states.
    """
    states = {}
    for qi, qname in enumerate(m1.states):
        m2.add_state(qi+offset)
        states[qname] = qi+offset
    for q in m1.transitions:
        for a in m1.transitions[q]:
            for t in m1.transitions[q][a]:
                m2.add_transition(nfa.Transition(states[t.q], t.a, states[t.r], t.action))
    return states[m1.start], {states[q] for q in m1.accept}
        
def union(m1, m2):
    """Returns a NFA that recognizes L(m1) \cup L(m2)."""
    m = nfa.NFA()
    start1, accept1 = copy_into(m1, m, offset=1)
    start2, accept2 = copy_into(m2, m, offset=1+len(m1.states))
    m.set_start(0)
    m.add_transition(nfa.Transition(0, nfa.EPSILON, start1))
    m.add_transition(nfa.Transition(0, nfa.EPSILON, start2))
    for q in accept1 | accept2:
        m.add_accept(q)
    return m

def concat(m1, m2):
    """Returns a NFA that recognizes L(m1) L(m2)."""
    m = nfa.NFA()
    start1, accept1 = copy_into(m1, m)
    start2, accept2 = copy_into(m2, m, offset=len(m1.states))
    m.set_start(start1)
    for q in accept1:
        m.add_transition(nfa.Transition(q, nfa.EPSILON, start2))
    for q in accept2:
        m.add_accept(q)
    return m

def star(m1):
    """Returns a NFA that recognizes L(m1)*."""
    m = nfa.NFA()
    start1, accept1 = copy_into(m1, m, offset=1)
    m.set_start(0)
    m.add_accept(0)
    m.add_transition(nfa.Transition(0, nfa.EPSILON, start1))
    for q in accept1:
        m.add_accept(q)
        m.add_transition(nfa.Transition(q, nfa.EPSILON, start1))
    return m

def group(m1, i):
    """Add open/close transitions."""
    m = nfa.NFA()
    m.set_start(0)
    m.add_accept(1)
    start1, accept1 = copy_into(m1, m, offset=2)
    m.add_transition(nfa.Transition(0, nfa.EPSILON, start1, ("begin", i)))
    for q in accept1:
        m.add_transition(nfa.Transition(q, nfa.EPSILON, 1, ("end", i)))
    return m

def backref(w):
    """Add copy k transiitions""" 
    m = nfa.NFA()
    m.set_start(0)
    m.add_transition(nfa.Transition(0, nfa.EPSILON, 1, ("copy", w)))
    # print(nfa.Transition(0, nfa.EPSILON, 1, ("copy", w)).action)
    m.add_accept(1)
    return m 
