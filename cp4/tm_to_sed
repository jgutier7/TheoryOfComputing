#!/usr/bin/env python3

import sys

# Read in the Turing machine description.

with open(sys.argv[1]) as tmfile:
    states = next(tmfile).split()
    input_symbols = next(tmfile).split()
    tape_symbols = next(tmfile).split()
    start_state = next(tmfile).strip()
    accept_state = next(tmfile).strip()
    reject_state = next(tmfile).strip()
    transitions = {}
    for line in tmfile:
        q, a, r, b, d = line.split()
        if q not in states or r not in states:
            raise ValueError("invalid state")
        if a not in tape_symbols or b not in tape_symbols:
            raise ValueError("invalid symbol")
        if d not in "LR":
            raise ValueError("invalid direction")
        transitions[q, a] = (r, b, d)

# These regular expressions, for any tape symbol and for any input
# symbol, respectively, get used over and over again.
        
gamma = "({})".format("|".join(tape_symbols))
sigma = "({})".format("|".join(input_symbols))

# Create start configuration, using a format similar to Sipser's.
print(r"s/(({sigma})*)/[{q}]\1/".format(sigma=sigma, q=start_state))

# Main loop
print(":loop")
for q in states:
    if q == accept_state: continue
    for a in tape_symbols:

        # Append blank if needed
        if a == "_":
            print(r"s/({gamma}*)[{q}]/\1[{q}]_/".format(gamma=gamma, q=q))

        # Convert transition into sed commands
        if (q, a) in transitions:
            r, b, d = transitions[q, a]
            if d == "L":
                print(r"s/({gamma}*)({gamma})[{q}]{a}({gamma}*)/\1[{r}]\g<3>{b}\5/".format(gamma=gamma, q=q, a=a, r=r, b=b))
                # handle left end of tape
                print(r"s/[{q}]{a}({gamma}*)/[{r}]\g<1>{b}\g<3>/".format(gamma=gamma, q=q, a=a, r=r, b=b))
            elif d == "R":
                print(r"s/({gamma}*)[{q}]{a}({gamma}*)/\g<1>{b}[{r}]\3/".format(gamma=gamma, q=q, a=a, r=r, b=b))

        # If no transition, go to reject state
        else:
            print(r"s/({gamma}*)[{q}]({a}{gamma}*)/\1[{qr}]\3/".format(gamma=gamma, q=q, a=a, qr=reject_state))

# If machine is in accept/reject state, branch to :accept/:reject;
# otherwise, loop
print("/{gamma}*[{q}]{gamma}*/baccept".format(gamma=gamma, q=accept_state))
print("/{gamma}*[{q}]{gamma}*/breject".format(gamma=gamma, q=reject_state))
print("/{gamma}*[({states})]{gamma}*/bloop".format(gamma=gamma, states='|'.join(states)))

# Accept: convert configuration to "accept:" followed by string
print(":accept")
print(r"s/({gamma}*)[{q}]({gamma}*)/accept:\1\3/".format(gamma=gamma,q=accept_state))
print("/{gamma}*/bhalt".format(gamma=gamma))

# Reject: replace configuration with "reject"
print(":reject")
print("s/{gamma}*[{q}]{gamma}*/reject/".format(gamma=gamma,q=reject_state))

print(":halt")

