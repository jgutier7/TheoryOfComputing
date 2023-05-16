#!/usr/bin/env python3

import regexp

def print_ast(node):
    op, *args = node
    if op in ["union", "concat", "star", "group"]:
        return "({} {})".format(op, " ".join(map(print_ast, args)))
    elif op == "epsilon":
        return "(epsilon)"
    elif op == "symbol":
        return '(symbol "{}")'.format(args[0])
    else:
        raise NotImplementedError(op)

if __name__ == "__main__":
    import sys
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('regexp', metavar='regexp', help='regular expression')
    args = argparser.parse_args()

    try:
        tree = regexp.parse(args.regexp)
    except regexp.ParseError as e:
        sys.stderr.write("parse error: {}\n".format(e))
        sys.exit(1)
    print(print_ast(tree))

