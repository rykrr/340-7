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
			slen += 1
			
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
                else:
                    clen += 1
	
	return (code, counts[clen:])


def hex_to_bits(hexes):
	bits = []
	
	if hexes == '':
		return
	
	value = int(hexes, 16)
	
	for i in range(32):
		bits.append((value >> (31-i)) & 1)
	
	return bits


def code_to_string(code):
	string = ''
	for codon in code.split(' '):
		if codon in decode_table:
			string += decode_table[codon]
		else:
			string += '(?)'
	return string



def decode(hexes, prev=[], dot=9, dash=27, space=30):
        #print()
	bits = hex_to_bits(hexes)
        #print('New:   {}'.format(bits))
	bits = prev + bits
        #print('Prev:  {}'.format(prev))
	bits = discard_leading_zeros(bits)
        #print('Fuse:  {}'.format(bits))
		
	if not len(bits):
		bits = counts_to_bits([1,32])
		return (('', ''), [])

	counts = bits_to_counts(bits)
        #print('COUNT: {}'.format(counts))
	
	(code, trailing) = counts_to_code(counts, dot, dash, space)
	string = code_to_string(code)
	
	#print("count: {}".format(trailing))
	#print("bits:  {}".format(counts_to_bits(trailing)))
	
	return ((code, string), counts_to_bits(trailing))
