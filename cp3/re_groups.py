#!/usr/bin/env python3

import regular
import nfa
import regexp
import sys

def swap(tree, group_count):

    for i in range(len(tree)):
        if tree[i] == 'group':
            tree[i + 1] = group_count
            group_count += 1

        if type(tree[i]) is list:
            _ , group_count = swap(tree[i], group_count)
                                  
              
    return tree, group_count

def re_groups(r, w):
    """If regexp matches string, prints accept followed by any matching groups, one per line
    Otherwise, prints reject"""
    tree = regexp.parse(r)
    group_count = 1
    tree, count  = swap(tree, group_count)
    m = regexp.to_nfa(tree)
    flag, path = nfa.match_dfs(m,w)

    
    groups = {}
    string = ''

    if not path:
        return None, None 
   
    for i in range(len(path)):
        #print(str(path[i].open1[0]) + str(path[i].open1[1]))
        #print(path[i].a)
        if path[i].open1[0] == 'open':
            num = path[i].open1[1]
            i += 1
            while True:
                if path[i].open1[0] == 'close' and path[i].open1[1] == num:
                    break
                if path[i].a != '&':
                    string += str(path[i].a)
                if i < len(path) - 2:
                   i += 1
                else:
                    break
            groups[num] = string
            string = ''
   
    return flag, groups

def main():
    regexp = sys.argv[1]
    string = sys.argv[2]
    flag, groups = re_groups(regexp, string)

    if flag == True:
        print('accept')
    else:
        print('reject')
        return 0

    for key in groups:
        print(str(key) + ':' + groups[key])

if __name__ == '__main__':
        main()
