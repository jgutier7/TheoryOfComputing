#!/usr/bin/env python3

import collections
import nfa
import regexp
import backref

verbose = False

if __name__ == "__main__":
    import argparse
    import fileinput
    import sys
    
    argparser = argparse.ArgumentParser()
    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', metavar='cmd', dest="cmds", action="append", help='command (can be used multiple times)')
    group.add_argument('-f', metavar='file', dest="cmdfile",  help='file containing commands')
    argparser.add_argument('input', nargs='*', metavar='input', help='input file(s)')
    argparser.add_argument('-v', dest="verbose", action="store_true", help="verbose output")
    args = argparser.parse_args()

    verbose = args.verbose

    # Parse the commands
    commands = []
    labels = {}
    if args.cmdfile:
        lines = [line.strip() for line in open(args.cmdfile)]
    elif args.cmds:
        lines = args.cmds
    
    for line in lines:
        line = line.strip()
        if line.startswith(":"):
            labels[line[1:]] = len(commands)
        else:
            fields = line.split("/")
            if len(fields) == 4 and fields[0] == "s" and fields[3] == "":
                find = regexp.to_nfa(regexp.parse(fields[1]))
                replace = backref.parse_backrefs(fields[2])
                commands.append(("s", find, replace))
            elif len(fields) == 3 and fields[0] == "" and fields[2].startswith("b"):
                find = regexp.to_nfa(regexp.parse(fields[1]))
                label = fields[2][1:]
                commands.append(("b", find, label))
            else:
                raise ValueError("invalid command {}".format(line))

    # Read and process the input lines
    for line in fileinput.input(args.input):
        w = list(line.rstrip('\n'))

        pc = 0
        while pc < len(commands):
            if verbose: print("{:4d}. {}".format(pc+1, "".join(w)))
            if commands[pc][0] == "s":
                flag, path = nfa.match(commands[pc][1], w)
                if flag:
                    begin = {}
                    end = {}
                    i = 0
                    for t in path:
                        if t.a != nfa.EPSILON:
                            i += 1
                        if t.action:
                            assert t.a == nfa.EPSILON
                            cmd, arg = t.action
                            if cmd == "begin":
                                begin[arg] = i
                            elif cmd == "end":
                                end[arg] = i
                    wnew = []
                    for tok in commands[pc][2]:
                        if isinstance(tok, backref.Backreference):
                            if tok.group in begin and tok.group in end:
                                wnew.extend(w[begin[tok.group]:end[tok.group]])
                        elif isinstance(tok, str):
                            wnew.append(tok)
                        else:
                            assert False
                    w = wnew
                pc += 1
            elif commands[pc][0] == "b":
                flag, _ = nfa.match(commands[pc][1], w)
                if flag:
                    pc = labels[commands[pc][2]]
                else:
                    pc += 1

        print("".join(w))
