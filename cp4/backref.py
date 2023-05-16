from collections import namedtuple

Backreference = namedtuple('Backreference', ['group'])

def parse_number(s, i):
    j = i
    while j < len(s) and s[j].isdigit():
        j += 1
    if j == i or s[i] == '0':
        raise ParseError('A backreference should be of the form \\ddd or \\g<ddd>, where ddd is one or more digits not starting with 0.')
    else:
        return int(s[i:j]), j

def parse_backrefs(s):
    tokens = []
    i = 0
    while i < len(s):
        if s[i:i+3] == '\\g<':
            n, i = parse_number(s, i+3)
            if i < len(s) and s[i] == '>':
                tokens.append(Backreference(n))
                i += 1
            else:
                raise ParseError('A backreference should be of the form \\ddd or \\g<ddd>, where ddd is one or more digits not starting with 0.')
        elif s[i] == '\\':
            n, i = parse_number(s, i+1)
            tokens.append(Backreference(n))
        else:
            tokens.append(s[i])
            i += 1
    return tokens
