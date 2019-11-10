#!/bin/python3

encode_table = {
	'':  '',
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


def counts_to_bits(counts):
	if not len(counts):
		return []
	
	bits = []
	
	for i, count in enumerate(counts):
		for j in range(count):
			bits.append(int(not (i%2)))
	
	return bits


def discard_leading_zeros(bits):
	if not len(bits):
		return []
	
	discard_count = 0
	
	for bit in bits:
		if bit == 1:
			break
		discard_count += 1
	
	return bits[discard_count:]


def counts_to_code(counts, dotlen, dashlen, spacelen):
	if not len(counts):
		return []
	
	code = ''
	clen = 0
	
	string = ''
	slen = 0
	
	binary_table = [['0', '1', '1'], ['', ' ', ' / ']]
	symbol_table = [['.', '-', '-'], ['', ' ', ' / ']]
	
	for i, count in enumerate(counts):
		if count >= spacelen:
			string += symbol_table[i%2][1]
			length += 1
			
			if i%2:
				code += string
				clen += slen
				string = ''
				slen = 0
		
		elif count >= dashlen:
			string += symbol_table[i%2][1]
			slen += 1
			
			if i%2:
				code += string
				clen += slen
				string = ''
				slen = 0
		
		elif count >= dotlen:
			string += symbol_table[i%2][0]
			slen += 1
	
	return (code, counts[clen:])


def hex_to_bits(hexes):
	bits = []
	
	for h in hexes:
		value = int(h, 16)
		
		for i in range(32):
			bits.append((value >> (31-i)) & 1)
	
	return bits


def code_to_string(code):
	string = ''
	for codon in code.split(' '):
		string += decode_table[codon]
	return string



def decode(hexes, prev=[], dot=1, dash=3, space=5):
	bits = hex_to_bits(hexes)
	bits = prev + bits
	bits = discard_leading_zeros(bits)
	counts = bits_to_counts(bits)
	
	(code, trailing) = counts_to_code(counts, dot, dash, space)
	string = code_to_string(code)
	
	return ((code, string), counts_to_bits(trailing))
