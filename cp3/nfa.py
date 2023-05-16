import collections

EPSILON = '&'

class Transition(object):
    def __init__(self, q, a, r, open1 = ['na', 0]):
        self.q = q
        self.a = a
        self.r = r
        self.open1 = open1
        

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

#match = match_dfs()
#match = match_bfs


