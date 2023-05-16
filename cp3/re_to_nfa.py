#!/usr/bin/env python3

import nfa
import regexp

if __name__ == "__main__":
    import argparse
    import sys
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    args = argparser.parse_args()

    try:
        tree = regexp.parse(args.regexp)
    except regexp.ParseError as e:
        sys.stderr.write("parse error: {}\n".format(e))
        sys.exit(1)
    groupnum = 0
    m = regexp.to_nfa(tree, groupnum)
    nfa.write(m, sys.stdout)
    

