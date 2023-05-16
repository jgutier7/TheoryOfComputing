#!/usr/bin/env python3
''' Grace Bezold, Jacob Gutierrez '''

import sys


BLANK = '_'

# variables for the sed function to replace the symbols to the left and right of the current symbol
BEFORE = 1
AFTER = 3



class TuringMachine:
	def __init__(self):
		self.states = set()
		self.inputSymbols = set()
		self.tapeSymbols = set()
		self.start_state = ""
		self.accept_state = ""
		self.reject_state = ""
		self.transitions = {}

	def set_states(self, states: list):
		for state in states:
			self.states.add(state)

	def set_inputs(self, inputSymbols: list):
		for symbol in inputSymbols:
			self.inputSymbols.add(symbol)

	def set_tape(self, tapeSymbols: list):
		for symbol in tapeSymbols:
			self.tapeSymbols.add(symbol)

	def set_start(self, start_state):
		self.start_state = start_state

	def set_accept(self, accept_state):
		self.accept_state = accept_state

	def set_reject(self, reject_state):
		self.reject_state =reject_state

	def set_transitions(self, transition):
		# transition[0] = current state, transition[1] = symbol the trasition reads
		# transition[2] = the state the transition goes to, transition[3] = the symbol the transition writes, transition[4] = the direction the transition moves the head
		self.transitions[(transition[0], transition[1])] = transition[2:]

	def tm_to_sed(self):
		''' outputs a msed script that is equivalent to the turing machine '''
		''' encodes states into string like Sipser  -> s/[TM TAPE]/[updating the tape]'''
		# creates a list of commands to be printed to the sed script
		c = self.create_commands()
		for command in c:
			print(command)
	
	def transition_to_branch(self, alpha_re, transition):		
		currState = transition[0]
		read	  = transition[1]
		newState  = transition[2]
		write	  = transition[3]
		move 	  = transition[4]
		# command =   /((a|b|_)*)       [q1]       a     ((a|b|_)*)  /b           q1Ra
		command = f'/(({alpha_re})*)[{currState}]{read}(({alpha_re})*)/b{currState}{move}{read}'	
		return command
	
	def transition_to_command(self, alpha_re, transition, left_most_cell):
		''' returns a sed command that is equivalent to the transition '''
		# transition[0] = current state, transition[1] = symbol the trasition reads
		currState = transition[0]
		read	  = transition[1]
		newState  = transition[2]
		write	  = transition[3]
		move 	  = transition[4]

		if move == 'R':
			# first line is the label for the transition (e.g. :q0R0)
			# second line is the sed command that replaces the current symbol on the tape with the write symbol
			# third line is the label for the next transition
			# replaces the current symbol on the tape (represented by the read variable) with the write symbol
			# moves the tape head to the right and updates the state to the newState.
			# groups (g<num>) are used to match the symbols to the left and right of the current symbol
			if currState == left_most_cell and write == BLANK and read == BLANK:
				# [q1]_ -> [q2]_[head] -> newState write
				# echo "" | msed -f <(tm_to_sed moveright.tm): FAILED (accept:__a != a__a)
				command = f':{currState}{move}{read}\n'\
					f's/(({alpha_re})*)[{currState}]{read}(({alpha_re})*)/\\g<{BEFORE}>[{newState}]{write}\\g<{AFTER}>{write}/\n'\
					f'/(({alpha_re})*)[{newState}](({alpha_re})*)/bloop'
				left_most_cell = newState
			elif newState == self.accept_state and currState == left_most_cell: # if we're on the farthest left cell and the transition is to the accept state
				command = f':{currState}{move}{read}\n'\
					f's/(({alpha_re})*)[{currState}]{read}(({alpha_re})*)/\\g<{BEFORE}>[{newState}]\\g<{AFTER}>{write}/\n'\
					f'/(({alpha_re})*)[{newState}](({alpha_re})*)/bloop'
			else: # the deault right transition
				command = f':{currState}{move}{read}\n'\
					f's/(({alpha_re})*)[{currState}]{read}(({alpha_re})*)/\\g<{BEFORE}>{write}[{newState}]\\g<{AFTER}>/\n'\
					f'/(({alpha_re})*)[{newState}](({alpha_re})*)/bloop'
		elif move == 'L':
			# replaces the symbol to the left of the tape head with the write symbol
			# moves the tape head to the left, and updates the state to the newState.
			if currState == left_most_cell: # check if at the leftmost symbol on the tape
				command = f':{currState}{move}{read}\n'\
						f's/(({alpha_re})*)[{currState}]{read}(({alpha_re})*)/\\g<{BEFORE}>[{newState}]{write}\\g<{AFTER}>/\n'\
						f'/(({alpha_re})*)[{newState}](({alpha_re})*)/bloop'
				left_most_cell = newState
			else: # the default left transition
				command = f':{currState}{move}{read}\n'\
					f's/(({alpha_re})*)({alpha_re})[{currState}]{read}(({alpha_re})*)/\\g<{BEFORE}>[{newState}]\\g<{AFTER}>{write}\\g<4>/\n'\
					f'/(({alpha_re})*)[{newState}](({alpha_re})*)/bloop'
		return left_most_cell, command
	
	def create_regex(self, items):
		# create a string that is a union of the items in the list to use in the sed script as a regex
		regex = items[0]
		for i in range(1, len(items)):
			regex += f"|{items[i]}"
		return regex
	
	def create_commands(self)->list:
		''' creates a list of commands to be printed to the sed script'''
		alpha  = list(self.tapeSymbols) # tape alphabet Γ
		states = list(self.states) # states Q
		accept = self.accept_state # accept state
		alpha_re = self.create_regex(alpha) # regex union of the tape alphabet
		state_re = self.create_regex([s for s in states if s != accept]) # regex union of the states except the accept state (used for the reject state)
		# transitions are stored as a dictionary with the key being a tuple of the current state and the symbol the transition reads
		transitions = [(key[0], key[1], value[0], value[1], value[2]) for key, value in self.transitions.items()]
		# create a list of commands to be printed to the sed script
		c = []

		# first line is the label for the start state (e.g. s/((a|b|_)*)/[q1]\1_/)
		# for example, if the original string is "aba_b"
		# the replacement string would be [q1]aba_b_ since the regex would match the entire string, and the underscore is appended to the end of the string to represent the blank symbol
		# this follows the format of the Sipser book
		c.append(f's/(({alpha_re})*)/[{self.start_state}]\\{BEFORE}{BLANK}/')

		# the loop label is used to loop back to the start of the sed script
		c.append(':loop')

		# under loop, set branches for each transition in the turing machine
		for transition in transitions:
			c.append(self.transition_to_branch(alpha_re, transition))

		# finally under the loop, check if the string is accepted or rejected, and branch to the appropriate label
		c.append(f'/(({alpha_re})*)[{accept}](({alpha_re})*)/baccept') # if the string ends in the accept state, the string is accepted
		c.append(f'/(({alpha_re})*)[({state_re})](({alpha_re})*)/breject') # if the string ends in a state other than the accept state, the string is rejected
		
		# for each transition, create a command with an appropriate label and append it to the list of commands
		left_most_cell = self.start_state
		for transition in transitions:
			left_most_cell, new_c = self.transition_to_command(alpha_re, transition, left_most_cell)
			c.append(new_c)
		
		# the accept and reject labels are used to determine if the string is accepted or rejected
		# c.append(f'/(({alpha_re})*)[{accept}](({alpha_re})*)/baccept') # if the string ends in the accept state, the string is accepted
		# c.append(f'/(({alpha_re})*)[({state_re})](({alpha_re})*)/breject') # if the string ends in a state other than the accept state, the string is rejected
		c.append(':accept') # label for the accept state
		c.append(f's/(({alpha_re})*)[{accept}](({alpha_re})*)/accept:\\g<{BEFORE}>\\g<{AFTER}>/') # replace the string with "accept:" followed by the string
		c.append('/accept/bexit') # if the string is accepted, end the sed script
		c.append(':reject') # label for the reject state
		c.append(f's/(({alpha_re})*)[({state_re})](({alpha_re})*)/reject/') # replace the string with "reject"
		c.append(':exit') # label for the end of the sed script

		# return the list of commands
		return c

def read_tm_file(filename)-> TuringMachine:
	with open(filename) as file:
		lines = file.readlines()
	file.close()
	transitions = []
	counter = 0
	TM = TuringMachine()
	for line in lines:
		if counter == 0:
			TM.set_states(line.split())
		if counter == 1:
			TM.set_inputs(line.split())
		if counter == 2:
			TM.set_tape(line.split())
		if counter == 3:
			TM.set_start(line.strip())
		if counter == 4:
			TM.set_accept(line.strip())
		if counter == 5:
			TM.set_reject(line.strip())
		if counter > 5:
			TM.set_transitions(line.split())
		counter += 1
	return TM

def main():
	# 	Accept a filename from the command line argument.
	file = sys.argv[1]
	# 	Read the Turing Machine description from the file using the read_tm() function defined above
	TM = read_tm_file(file)	
	# 	Convert the Turing Machine to a msed script using the tm_to_sed() function defined above
	TM.tm_to_sed()

if __name__ == "__main__":
	main()