# -*- coding: cp1251 -*- import sys import struct
import struct


def intToStrHex(val):
	''' (int) -> str

		Преобразование целого числа в строку HEX.

		>>> intToStrHex(12)
		'0C'
		>>> intToStrHex(2048)
		'0800'
	'''
	val = "%x" % val
	if len(val) % 2 == 1:
		val = '0' + val
	return val


def strHexToInt(val):
	''' (str) -> int

		Преобразование строки HEX в целое число.

		>>> strHexToInt("CC0")
		3264
		>>> strHexToInt("12")
		18
'''
	return int(val, 16)


def charToStrHex(val):
	''' (str) -> str
		Преобразование символов в строку hex.

		>>> charToStrHex('1')
		'31'
		>>> charToStrHex('A')
		'41'
		>>> charToStrHex('123')
		'313233'
	'''
	return val.encode('hex')


def strHexToChar(val):
	''' (str) -> str

		Преобразование строки HEX в символы.

		>>> '31'.decode('hex')
		'1'
		>>> '41'.decode('hex')
		'A'
		>>> "313233".decode('hex')
		'123'
	'''
	return val.decode('hex')


def hexToFloat(s, arch="big-endian"):
	''' (str) -> float
		
		Возвращает float полученный hex-cтрокой.
		@param arch выбор архитектуры
		@arg "little-endian" младшим байтом вперед
		@arg "big-endian" старшим байтом вперед
		
		>>> hexToFloat("41973333")
		18.899999618530273
		>>> hexToFloat("41973333", "little-endian")
		4.18142498403995e-08
		>>> hexToFloat("470FC614")
		36806.078125
	'''
	bins = ''.join(chr(int(s[x:x + 2], 16)) for x in range(0, len(s), 2))
	if arch == "little-endian":
		arch = '<f'
	elif arch == "big-endian":
		arch = '>f'
	else:
		print u"Error:",
		print u"Выбрана неверная архитектура"
		raise ValueError
	return struct.unpack(arch, bins)[0]


def floatToHex(val, arch="big-endian"):
	''' (float) -> str

		Возвращает float преобразованный в hex-строку.
		@param arch выбор архитектуры
		@arg "little-endian" младшим байтом вперед
		@arg "big-endian" старшим байтом вперед
		
		>>> floatToHex(3.99)
		"407f5c29"
		>>> floatToHex(3.99, "little-endian)
		"295C7F40"
		>>> floatToHex(12.18)
		"4142e148"
	'''
	if arch == "little-endian":
		arch = '<f'
	elif arch == "big-endian":
		arch = '>f'
	else:
		print u"Error:",
		print u"Выбрана неверная архитектура"
		raise ValueError
	s = struct.pack(arch, val)
	return ''.join('%.2x' % ord(c) for c in s).upper()
		
if __name__ == '__main__':
	import sys
	
	args = sys.argv
	for arg in args:
		if arg == '/?':
			print u'Справка:'
