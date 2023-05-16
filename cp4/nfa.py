#!/usr/bin/env python3
import sys
import collections

EPSILON = '&'

class Transition(object):
    def __init__(self, q, a, r, action=set()):
        self.q = q
        self.a = a
        self.r = r
        self.action = action # Used to open/close groups
      
class NFA(object):
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.start = None
        self.accept = set()
        self.transitions = {}

    def add_state(self, q):
        self.states.add(q)

    def add_symbol(self, a):
        self.alphabet.add(a)
        
    def set_start(self, q):
        self.add_state(q)
        self.start = q

    def add_accept(self, q): 
        self.add_state(q)
        self.accept.add(q)

    def add_transition(self, t):
        self.add_state(t.q)
        if t.a != EPSILON:
            self.add_symbol(t.a)
        self.add_state(t.r)
        self.transitions.setdefault(t.q, {}).setdefault(t.a, []).append(t)

def read(file):
    """Read a NFA from a file."""
    m = NFA()
    for q in next(file).split():
        m.add_state(q)
    for a in next(file).split():
        m.add_symbol(a)
    m.set_start(next(file).rstrip())
    for q in next(file).split():
        m.add_accept(q)
    for line in file:
        q, a, r = line.split()
        m.add_transition(Transition(q, a, r))
    return m

def write(m, file):
    """Write a NFA to a file."""
    file.write(' '.join(map(str, m.states)) + '\n')
    file.write(' '.join(map(str, m.alphabet)) + '\n')
    file.write(str(m.start) + '\n')
    file.write(' '.join(map(str, m.accept)) + '\n')
    for q in m.transitions:
        for a in m.transitions[q]:
            for t in m.transitions[q][a]:
                if t.action:
                    file.write("{} {} {} # {}\n".format(t.q, t.a, t.r, t.action))
                else:
                    file.write("{} {} {}\n".format(t.q, t.a, t.r))

def _transitions(m, w, q, i):
    """Helper function for match_dfs and match_bfs.

    If NFA m is in state q and reading string w at position i,
    iterates over possible transitions and new positions."""
    
    for t in m.transitions.get(q, {}).get(EPSILON, []):
        yield t, i
    if i < len(w):
        for t in m.transitions.get(q, {}).get(w[i], []):
            yield t, i+1

def match_dfs(m, w):
    """Test whether a NFA accepts a string.

    m: NFA
    w: list of symbols
    Returns: 
      - if m accepts w, then (True, path), where path is a list of Transitions
      - otherwise, (False, None)
    """
    
    visited = set() # Nodes that have been visited
    def visit(q, i):
        """Search starting from state q and position i."""
        if (q, i) in visited:
            return False, None
        visited.add((q, i)) # Do this before recursive calls, to avoid epsilon cycles
        if q in m.accept and i == len(w):
            return True, []
        for t, j in _transitions(m, w, q, i):
            flag, path = visit(t.r, j)
            if flag:
                path.append(t) # Build up path in reverse order
                return True, path
        return False, None

    flag, path = visit(m.start, 0)
    if flag:
        path.reverse()
    return (flag, path)

def match_bfs(m, w):
    """Test whether a NFA accepts a string.

    m: NFA
    w: list of symbols
    Returns: 
      - if m accepts w, then (True, path), where path is a list of Transitions
      - otherwise, (False, None)
    """

    if m.start in m.accept and len(w) == 0:
        return True, []
    start = (m.start, 0)
    frontier = collections.deque([start]) # Queue of configurations to explore
    visited = {} # Mapping from each visited configuration to one of its incoming transitions

    while len(frontier) > 0:
        q, i = frontier.popleft()
        for t, j in _transitions(m, w, q, i):
            # Don't allow duplicates in frontier.
            # If we do this later, it will be exponential.
            if (t.r, j) in visited: continue
            visited[t.r, j] = t
            if t.r in m.accept and j == len(w):
                # Reconstruct the path in reverse
                path = []
                r = t.r
                while (r, j) != start:
                    t = visited[r, j]
                    path.append(t)
                    r = t.q
                    if t.a != EPSILON: j -= 1
                path.reverse()
                return True, path
            frontier.append((t.r, j))
    return False, None

def add_group_configs():
    # loop thorugh m
    # adding 
    pass

def match_backref_dfs(m, w):
    """Test whether a NFA accepts a string.

    m: NFA
    w: list of symbols
    Returns: 
      - if m accepts w, then (True, path), where path is a list of Transitions
      - otherwise, (False, None)
    """
    # write(m, sys.stderr)
    visited = set()  # Nodes that have been visited
    def visit(q, i, start, end):
        # print( q, i, start, end)
        """Search starting from state q and position i."""
        if (q, i, frozenset(start.items()), frozenset(end.items())) in visited:
            return False
        visited.add((q, i, frozenset(start.items()), frozenset(end.items())))

        # ifff the NFA has reached an accepting state and the string has been fully processed, return True
        if q in m.accept and i == len(w):
            return True
        # loop thorugh each possible transition from this state
        for t, j in _transitions(m, w, q, i):
            # print(q, t.r)
            if t.action: # Action associated with the transition (if any)
                cmd, g = t.action
                g = int(g)
            else:
                cmd, g = None, None

            # print(t.action) 
            # creates copies of start and end dictionaries to avoid overwriting
            new_start, new_end = dict(start), dict(end)  # Create a copy of start and end dictionaries to avoid overwriting

            if cmd == "begin": # the action is "begin", update the start dictionary
                new_start[g] = i
            elif cmd == "end": # same witht he end 
                new_end[g] = i


            if cmd == "copy":
                # print("in copy")
                # Check if group is in the string
                try:
                    prev_group_match = w[new_start[g]:new_end[g]]  # previous group match in the string 
                    next_match = w[i: i + len(prev_group_match)] # next possible group match in the string
                    # print(prev_group_match)
                    # print(next_match)
                    if (i - 1 + len(prev_group_match)) < len(w) and next_match == prev_group_match:
                        # Create new configuration (r, i + len(prev_group_match))
                        j = i + len(prev_group_match)
                    else:
                        continue
                except:
                    j=j
                    
             # recursively visit the next state with the updated start and end dictionaries
            flag = visit(t.r, j, new_start, new_end)
            if flag:
                return True
            
        #return False
        #non-epsilon transitions
        # if i < len(w):
        #     for t, j in _transitions(m, w, q, i):
        #         if 

    # start the visit at the beginning , sending in empty dictionaries for start and end 
    flag = visit(m.start, 0, {}, {})
    return flag


#path = sys.argv[1] # gets the file path to the NFA
#w    = sys.argv[2] # gets the string to match 
#file = open(path)
#M    = read(file)

#match_backref_dfs(M,w)
#match = match_bfs

# def match_backref_dfs(m, w):
#     """Test whether a NFA accepts a string.
#     m: NFA
#     w: list of symbols
#     Returns: 
#       - if m accepts w, then (True, path), where path is a list of Transitions
#       - otherwise, (False, None)
#     """
#     start = {}
#     end = {}
#     visited = [] # Nodes that have been visited # lists of lists (q,i,gnum,start,end)

#     def visit(q, i, group_num, start, end):
#         """Search starting from state q and position i."""
#         if (q, i, group_num, start, end) in visited:
#             return False, None
#         visited.append((q, i, group_num, start, end))

#         for t, j in _transitions(m, w, q, i):       
#             try:
#                 cmd, g = t.action
#             except:
#                 continue
#             if "begin" in t.action:
#                 start[g] = i
#             elif "end" in t.action:
#                 end[g] = i
           
#             if "copy" in t.action:
#                 g = int(g)
#                 prev_group_match = w[start[g]:end[g]]
#                 if w[i: i + len(prev_group_match) - 1] == prev_group_match:
#                     #create new configuration (r, i+len(gk))
#                     i = i+len(prev_group_match)
#                 else:
#                     continue

#             will_accept = visit(t.r, i, g, start, end)
#             if will_accept:
#                 return True
#         # if i < len(w):
#         #     for t, j in _transitions(m, w, q, i):
#         #         #print(f't: {t} j: {j}')
#         #         flag = visit(t.r, j, group_num, start, end)
#         #         if flag:
#         #             return True

#         #visited.append((q, i, group_num, start, end)) # Do this before recursive calls, to avoid epsilon cycles
#         if q in m.accept and i == len(w):
#             return True


#         return False

#     flag = visit(m.start, 0, 1, start, end)
#     return (flag)