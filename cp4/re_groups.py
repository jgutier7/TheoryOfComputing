#!/usr/bin/env python3

import nfa
import regexp

if __name__ == "__main__":
    import argparse
    import fileinput
    import sys
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    argparser.add_argument('input', metavar='string', help='input string')
    args = argparser.parse_args()

    alpha = regexp.parse(args.regexp)
    m = regexp.to_nfa(alpha)
    w = args.input

    flag, path = nfa.match(m, w)
    if flag:
        print("accept")
        begin = {}
        end = {}
        i = 0
        for t in path:
            if t.a != nfa.EPSILON:
                i += 1
            if t.action:
                cmd, g = t.action
                if cmd == "begin":
                    begin[g] = i
                elif cmd == "end":
                    end[g] = i
        for i in sorted(begin):
            print("{}:{}".format(i, w[begin[i]:end[i]]))
    else:
        print("reject")
        
