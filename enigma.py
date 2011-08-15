import random
import copy
ALPHABET = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", " "]

class Scrambler(object):
	"""A single scrambler unit"""
	def __init__(self, seed):
		super(Scrambler, self).__init__()
		self.routes = range(len(ALPHABET))
		random.seed(seed)
		random.shuffle(self.routes)
	
	def __str__(self):
		s = ''
		for i in range(len(ALPHABET)):
			s += '%s %i => %i\n' % (ALPHABET[i], i, self.routes[i])
		return s
	
	def forward(self, index):
		return self.routes[index]
	
	def backwards(self, index):
		return self.routes.index(index)

class EnigmaMachine(object):
	"""An enigma machine that uses some Scramblers"""
	def __init__(self):
		super(EnigmaMachine, self).__init__()
		self.scramblers = []
		self.offsets = []
		self.alphabet = ALPHABET
	
	def addScrambler(self, scrambler, offset):
		self.scramblers.append(scrambler)
		self.offsets.append(offset)
	
	def setPlugboardReplacement(self, a, b):
		self.alphabet[self.alphabet.index(a)] = b
		self.alphabet[self.alphabet.index(b)] = a
	
	def isReady(self):
		return len(self.scramblers) >= 1
	
	def reset(self):
		self.scramblers = []
		self.offsets = []
		self.alphabet = ALPHABET
	
	def scramble(self, char):
		# For each scrambler, apply offset and trace through
		char = self.alphabet.index(char.upper())
		for i in range(len(self.scramblers)):
			char = (char + self.offsets[i]) % len(ALPHABET)
			char = self.scramblers[i].forward(char)
		char = (len(ALPHABET) - 1) - char
		for i in reversed(range(len(self.scramblers))):
			char = self.scramblers[i].backwards(char)
			char = (char - self.offsets[i]) % len(ALPHABET)
		# Tick all scramblers on if required
		for i in range(len(self.offsets)):
			if i == 0:
				self.offsets[i] += 1
			else:
				if self.offsets[i - 1] == 0:
					self.offsets[i] += 1
		return self.alphabet[char]
		
def test():
	result = "HELLO => "
	e = EnigmaMachine()
	e.addScrambler(Scrambler(1), 10)
	e.addScrambler(Scrambler(2), 100)
	e.addScrambler(Scrambler(3), 1000)
	e.setPlugboardReplacement("H", "E")
	for s in "HELLO WORLD":
		result += e.scramble(s)
	result += " => "
	e = EnigmaMachine()
	e.addScrambler(Scrambler(1), 10)
	e.addScrambler(Scrambler(2), 100)
	e.addScrambler(Scrambler(3), 1000)
	e.setPlugboardReplacement("H", "E")
	for s in "EIBDUCKTPCU":
		result += e.scramble(s)
	print result


if __name__ == '__main__':
	e = EnigmaMachine()
	while (True):
		print "+> ",
		command = str(raw_input()).upper()
		if command.startswith("NEW") or command.startswith("RESET"):
			e.reset()
			print " #  Machine configuration reset"
		elif command.startswith("ADD"):
			params = command.replace("ADD", "").replace(" ", "").split(":")
			e.addScrambler(Scrambler(int(params[0])), (ALPHABET.index(params[1]) % len(ALPHABET)))
		elif command.startswith("SWAP"):
			params = command.replace("SWAP", "").replace(" ","").split(":")
			e.setPlugboardReplacement(params[0], params[1])
		elif command.startswith(":"):
			if e.isReady():
				plaintext = command.replace(":", "")
				cyphertext = ''
				for s in plaintext:
					if s in ALPHABET:
						cyphertext += e.scramble(s)
				print cyphertext
			else:
				print " #  Machine not configured!"
		elif command.startswith("HELP"):
			print """ # Commands:
 #  new          => resets the machine configuration
 #  reset        => resets the machine configuration
 #  add <a>:<b>  => adds the scrambler with id <id> and oriented to face the letter <orientation
 #  swap <a>:<b> => swaps the letters <a> and <b> on the virtual plugboard
 #  :<plaintext> => scrambles the given plaintext
 #    this will also decrypt a given cyphertext as long as the settings are the same
 #  
 #  test         => runs a test encrypt/decrypt and outputs the result
 #  help         => prints this message
 #  exit         => exits the script"""
		elif command.startswith("TEST"):
			test()
		elif command.startswith("EXIT"):
			exit()
	