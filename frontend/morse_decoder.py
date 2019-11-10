#!/bin/python3

encode_table = {
	' ': '/',
	'e': '.',
	't': '-',
	'i': '..',
	'a': '.-',
	'n': '--',
	's': '...',
	'u': '..-',
	'r': '.-.',
	'w': '.--',
	'd': '-..',
	'k': '-.-',
	'g': '--.',
	'o': '---',
	'h': '....',
	'v': '...-',
	'f': '..-.',
	'l': '.-..',
	'p': '.--.',
	'j': '.---',
	'b': '-...',
	'x': '-..-',
	'c': '-.-.',
	'y': '-.--',
	'z': '--..',
	'q': '--.-'
}

decode_table = { val: key for key, val in encode_table.items() }

def bits_to_counts(bits):
	if not len(bits):
		return []
	
	counts = []
	count  = 0
	
	state = bits[0]
	
	for bit in bits:
		if bit == state:
			count += 1
		else:
			state = bit
			counts.append(count)
			count = 1
	
	counts.append(count)
	return counts


def discard_leading_zeros(bits):
	if not len(bits):
		return []
	
	discard_count = 0
	
	for bit in bits:
		if bit == 1:
			break
		discard_count += 1
	
	return bits[discard_count:]


def counts_to_code(counts, dotlen, dashlen, spacelen, error):
	if not len(counts):
		return []
	
	code = ''
	bits = 0
	size = 0
	
	letters = []

	binary_table = [['0', '1', '1'], ['', ' ', ' / ']]
	symbol_table = [['.', '-', '-'], ['', ' ', ' / ']]
	
	for i, count in enumerate(counts):
		if count in range(dotlen - error, dotlen + error):
			code += symbol_table[i%2][0]
			
		elif count in range(dashlen - error, dashlen + error):
			code += symbol_table[i%2][1]
		
		elif count in range(spacelen - error, spacelen - error):
			code += symbol_table[i%2][1]
	
	return code


def hex_to_bits(hexes):
	value = int(hexes, 16)
	bits = []
	
	for i in range(32):
		bits.append((value >> (31-i)) & 1)
	
	return bits


def words_to_string(words):
	string = ''
	
	for word in words:
		for letter in word:
			for symbol in word:
				if symbol == 0:
					string += '-'
				else:
					string += '.'
		string += ' '
	string += '/ '
	
	return string


def code_to_string(code):
	string = ''
	for codon in code.split(' '):
		string += decode_table[codon]
	return string

sos = [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
b = discard_leading_zeros(sos)
c = bits_to_counts(b)
C = counts_to_code(c, 1, 3, 7, 1)

print(code_to_string(C))
