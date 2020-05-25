#!/usr/bin/python3 -OO


ucode_trans = {
'Á': 'A', 'á': 'a',
'Ä': 'A', 'ä': 'a',
'É': 'E', 'é': 'e',
'Í': 'I', 'í': 'i',
'Ó': 'O', 'ó': 'o',
'Ö': 'O', 'ö': 'o',
'Ő': 'O', 'ő': 'o',
'Ú': 'U', 'ú': 'u',
'Ü': 'U', 'ü': 'u',
'Ű': 'U', 'ű': 'u',
'ß': 'ss',
}


u8code_trans = {
'\xC1': 'A', '\x8F': 'A', '\x9F': 'A', '\xC4': 'A', '\xC5': 'A',
'\xE0': 'a', '\xE1': 'a', '\xA0': 'a', '\xE4': 'a', '\x83': 'a',
'\xE7': 'c',
'\xC9': 'E', '\x90': 'E',
'\xE8': 'e', '\xE9': 'e', '\x82': 'e', '\xEA': 'e', '\x88': 'e',
'\xCD': 'I', '\xAD': 'I',
'\xED': 'i', '\xEF': 'i',
'\xD3': 'O', '\xD6': 'O', '\xD5': 'O',
'\xF3': 'o', '\xF6': 'o', '\xF5': 'o',
'\xDA': 'U', '\x9A': 'U', '\xDC': 'U',
'\x96': 'u', '\xFA': 'u', '\xFC': 'u', '\xFB': 'u',
'\x84': '\'', '\x94': '\'',
'\xC3': 'x',
'\xDF': 'ss',
'\xB6': 'f'
}


def udec(word):
	sout = ""
	for c in word:
		if c in ucode_trans:
			sout += ucode_trans[c]
		else:
			sout += c
	return sout


def nouc(word):
	sout = u""
	i = 0
	while i < len(word):
		if word[i] == 0xE0 or word[i] == 0xE1 or word[i] == 0xA0 or word[i] == 0xE4 or word[i] == 0x83 or word[i] == 0xC1 or word[i] == 0x8F or word[i] == 0x9F or word[i] == 0xC4 or word[i] == 0xC5:
			sout += 'a'
		elif word[i] == 0xE7:
			sout += 'c'
		elif word[i] == 0xE8 or word[i] == 0xE9 or word[i] == 0x82 or word[i] == 0xEA or word[i] == 0x88 or word[i] == 0xC9 or word[i] == 0x90:
			sout += 'e'
		elif word[i] == 0xED or word[i] == 0xEF or word[i] == 0xCD or word[i] == 0xAD:
			sout += 'i'
		elif word[i] == 0xF1:
			sout += 'n'
		elif word[i] == 0xF3 or word[i] == 0xF6 or word[i] == 0xF5 or word[i] == 0xD3 or word[i] == 0xD6 or word[i] == 0xD5:
			sout += 'o'
		elif word[i] == 0x96 or word[i] == 0xFA or word[i] == 0xFC or word[i] == 0xFB or word[i] == 0xDA or word[i] == 0x9A or word[i] == 0xDC:
			sout += 'u'
		elif word[i] == 0x9C:
			sout += '£'
		elif word[i] == 0x84 or word[i] == 0x94:
			sout += '\''
		elif word[i] == 0xC3:
			sout += 'x'
		elif word[i] == 0xB6:
			sout += 'f'
		elif word[i] == 0xDF:
			sout += 'ss'
		elif word[i] == ord('\n') or word[i] == ord('\r'):
			break
		else:
			sout += chr(word[i]).lower()
		i += 1
	return sout

def uc(word):
	sout = u""
	i = 0
	while i < len(word):
		if word[i] == 0xE0:
			sout += 'à'
		elif word[i] == 0xE1 or word[i] == 0xA0:
			sout += 'á'
		elif word[i] == 0xE4:
			sout += 'ä'
		elif word[i] == 0x83:
			sout += 'â'
		elif word[i] == 0xE7:
			sout += 'ç'
		elif word[i] == 0xE8:
			sout += 'è'
		elif word[i] == 0xE9 or word[i] == 0x82:
			sout += 'é'
		elif word[i] == 0xEA or word[i] == 0x88:
			sout += 'ê'
		elif word[i] == 0xED:
			sout += 'í'
		elif word[i] == 0xEF:
			sout += 'ï'
		elif word[i] == 0xF1:
			sout += 'ñ'
		elif word[i] == 0xF3:
			sout += 'ó'
		elif word[i] == 0xF6:
			sout += 'ö'
		elif word[i] == 0xF5:
			sout += 'ő'
		elif word[i] == 0x96:
			sout += 'û'
		elif word[i] == 0xFA:
			sout += 'ú'
		elif word[i] == 0xFC:
			sout += 'ü'
		elif word[i] == 0xFB:
			sout += 'ű'
		elif word[i] == 0xC1 or word[i] == 0x8F or word[i] == 0x9F:
			sout += 'Á'
		elif word[i] == 0xC4:
			sout += 'Ä'
		elif word[i] == 0xC5:
			sout += 'Å'
		elif word[i] == 0xC9 or word[i] == 0x90:
			sout += 'É'
		elif word[i] == 0xCD or word[i] == 0xAD:
			sout += 'Í'
		elif word[i] == 0xD3:
			sout += 'Ó'
		elif word[i] == 0xD6:
			sout += 'Ö'
		elif word[i] == 0xDA:
			sout += 'Ú'
		elif word[i] == 0x9A or word[i] == 0xDC:
			sout += 'Ü'
		elif word[i] == 0x9C:
			sout += '£'

		elif word[i] == 0x84 or word[i] == 0x94:
			sout += '\''
		elif word[i] == 0xC3:
			sout += 'x'
		elif word[i] == 0xB6:
			sout += 'F'
		elif word[i] == 0xDF:
			sout += 'ß'

		elif word[i] == ord('\n') or word[i] == ord('\r'):
			break
		else:
			if word[i] > ord('z') and word[i] != 126 and word[i] != 123 and word[i] != 125:
				print(word, "[", i, "]: ", word[i])
			sout += chr(word[i])
		i += 1
	return sout
