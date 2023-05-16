#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Adding backreferences to regular expressions increases their power a lot; in fact, it makes matching NP-complete. 
# This is a program that demonstrates this by reducing Boolean satisfiability to regular expression matching with backreferences.

import sys
import re   
import os
import argparse


def mapping(cnf):

    num_vars = 0
    clause_count = 0
    null_count = {1: 'false'}
    backref = {}

    for i in range(len(cnf) - 1):
        #get number of variables
        if cnf[i] == 'x':
            if cnf[i + 1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                if int(num_vars) < int(cnf[i+1]):
                    num_vars = cnf[i + 1]
            else:
                num_vars = 1
        if cnf[i] == '&':
            clause_count += 1
        if cnf[i] == '!':
            if cnf[i + 2] in ('1','2','3','4','5','6','7','8','9'):
                null_count[int(cnf[i+2])] = 'true'
            else:
                null_count[1] = 'true'
        
    #make regexp
    regexp = ''
    string = ''
    backref_count = 1
    if num_vars == 1:
        if null_count[1] == 'false':
            regexp += '(1)'
            backref[backref_count] = 1
            backref_count += 1
        else:
            regexp += '((1)|(1))'
            backref[backref_count] = 2
            backref_count += 1
            backref[backref_count] = 3
        string += '1'
    else:      
        for i in range(int(num_vars)):
            if null_count[i + 1] == 'false':
                regexp += '(1)'
                backref[backref_count] = 1
                backref_count += 1
            else:
                regexp += '((1)|(1))'
                backref[backref_count] = 3*(i + 1) - 1
                backref_count += 1
                backref[backref_count] = 3*(i+1)
                backref_count += 1

            string += '1'

    if clause_count > 0:
            clause_count += 1

            #second part of regexp w/ backrefs
            for i in range(len(cnf) - 1):
                if cnf[i] == '(':
                    regexp += '#('
                if cnf[i] == ')':
                    regexp += ')'
                #deal with !
                if cnf[i] == 'x':
                    if cnf[i + 1] in ('1','2'):
                        num = int(cnf[i + 1])
                        if int(cnf[i + 1]) > 1 and null_count[int(cnf[i + 1]) - 1] == 'true':
                            num += 1
                    else:
                        num = 1
                    if cnf[i - 1] == '!':
                        num += 1
                    regexp += '('
                    regexp += '\\'
                    #print(num)
                    #print(backref[num])
                    regexp += str(backref[num])
                    regexp += ')'

                if cnf[i] == '|':
                    regexp += '|'
                            
    
            regexp += ')'

        #finish string
            if clause_count > 0:
                clause_count += 1
                for i in range(clause_count - 1):
                    string += '#'
                    string += '1'

    return regexp, string


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('cnf', metavar='cnf', help='cnf formula')
    args = argparser.parse_args()
    
    regexp, string = mapping(args.cnf)
    print('regexp:' + regexp)
    print('string:' + string)