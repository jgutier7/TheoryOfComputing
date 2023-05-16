#!/usr/bin/env python3

import nfa
import regexp
import pdb

if __name__ == "__main__":
    import argparse
    import fileinput
    import sys
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    argparser.add_argument('input', nargs='*', metavar='input', help='input file(s)')
    args = argparser.parse_args()

    try:
        tree = regexp.parse(args.regexp)
    except regexp.ParseError as e:
        sys.stderr.write("parse error: {}\n".format(e))
        sys.exit(1)
    m = regexp.to_nfa(tree)

    for line in fileinput.input(args.input):
        w = line.rstrip('\n')
        flag, _ = nfa.match_backref_dfs(m, w)
        if flag:
            pdb.set_trace()
            print(w, flush=True)