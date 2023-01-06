import configparser

class EnigmaMachine:

	def rotator(self, alphabet):
		return alphabet[-1] + alphabet[0:-1]

	def rotate(self):
		self.ring1 += 1
		self.rotor1 = self.rotator(self.rotor1)
		if self.ring1 > len(self.alpha):
			self.ring1 = 1
			self.ring2 += 1
			self.rotor2 = self.rotator(self.rotor2)
			if self.ring2 > len(self.alpha):
				self.ring2 = 1
				self.ring3 += 1
				self.rotor3 = self.rotator(self.rotor3)
				if self.ring3 > len(self.alpha):
					self.ring3 = 1

	def apply_settings(self):
		self.info = {
			self.rotor1: self.ring1,
			self.rotor2: self.ring2,
			self.rotor3: self.ring3
		}

		for key in self.info:

			rotor_output = key
			for i in range(self.info[key] - 1):
				rotor_output = self.rotator(rotor_output)

			self.outlist.append(rotor_output)

		self.rotor1 = self.outlist[0]
		self.rotor2 = self.outlist[1]
		self.rotor3 = self.outlist[2]


	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		wheel_order   = config['setting']['wheelOrder'].split(' ')
		ring_settings = config['setting']['ringsOffset'].split(' ')
		self.outlist  = []
		self.alpha    = config['alphabet']['alphabet']

		# set ring settings
		self.ring1  = int(ring_settings[0])
		self.ring2  = int(ring_settings[1])
		self.ring3  = int(ring_settings[2])

		# set rotors
		self.rotor1 = config['rotors'][wheel_order[0]]
		self.rotor2 = config['rotors'][wheel_order[1]]
		self.rotor3 = config['rotors'][wheel_order[2]]

		# plugboard
		self.plugboard = config['setting']['plugboardConnections'].split(' ')

		self.apply_settings()


	def show(self):
		print('rotor1', self.rotor1)
		print('rotor2', self.rotor2)
		print('rotor3', self.rotor3)
		print('ring1', self.ring1)
		print('ring2', self.ring2)
		print('ring3', self.ring3)


	def reflector(self, char):
		return self.alpha[(self.alpha.find(char) * -1) -1]


	def rotor3f(self, char):
		find_char = self.rotor3[self.alpha.index(char)]
		get_char  = self.reflector(find_char)
		out_char  = self.alpha[self.rotor3.index(get_char)]
		return out_char


	def rotor2f(self, char):
		find_char = self.rotor2[self.alpha.index(char)]
		get_char  = self.rotor3f(find_char)
		out_char  = self.alpha[self.rotor2.index(get_char)]
		return out_char

	def rotor1f(self, char):
		if char not in self.alpha: return char
		find_char = self.rotor1[self.alpha.index(char)]
		get_char  = self.rotor2f(find_char)
		out_char  = self.alpha[self.rotor1.index(get_char)]
		self.rotate()
		return out_char

	def replace(self, char):
		for plug in self.plugboard:
			if char in plug:
				if plug.upper().index(char.upper()) == 0:
					out_char = self.rotor1f(plug[1])
					return out_char
				else:
					out_char = self.rotor1f(plug[0])
					return out_char
			else:
				out_char = self.rotor1f(char)
				return out_char

def Enigma(message):
	config = configparser.ConfigParser()
	config.read('config.ini')
	alphabet = config['alphabet']['alphabet']
	p, output = EnigmaMachine(), ''
	for i in message:
		if i.lower() not in alphabet and i != '\n': continue
		output += p.replace(i)

	return output



