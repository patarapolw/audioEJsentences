from openpyxl import *
import sys, os
from random import randint
from time import sleep
from bs4 import BeautifulSoup

level = 'SpoonFed'
lang = 'cn' #cn or jp

if lang == 'cn':
	speaker = 'ting-ting'
	level_type = 'HSK'
	en_col = 'C'
	lang_col = 'A'

if lang == 'jp':
	speaker = 'kyoko'
	level_type = 'JLPT'
	en_col = 'B'
	lang_col = 'A'

if level == 'SpoonFed':
	en_col = 'A'
	lang_col = 'C'

def printAnything(anything):
	sys.stdout.buffer.write((repr(anything) + '\n').encode('utf8'))

def printText(text):
	sys.stdout.buffer.write((text + '\n').encode('utf8'))

def say(sentence, speaker):
	os.system('say -v {} "{}"'.format(speaker, sentence))

def sayTemplate(row):
	global sheet, max_row, speaker, en_col, lang_col

	en_sen = sheet[en_col + str(row)].value
	if en_sen == None:
		return
	lang_sen = sheet[lang_col + str(row)].value
	
	print()
	print('Saying row:', row, 'of', max_row)
	en_sen = BeautifulSoup(en_sen, 'lxml').text
	printAnything(en_sen)
	say(en_sen, 'alex')
	sleep(2) #in seconds

	lang_sen = BeautifulSoup(lang_sen, 'lxml').text
	printText(lang_sen)
	say(lang_sen, speaker)
	sleep(1)

def sayRandom(num_sen):
	global max_row

	print('Number of sentences to say:', num_sen)

	for i in range(num_sen):
		row = randint(2,max_row)
		sayTemplate(row)

def sayAll(start=2):
	global max_row

	print('Number of sentences to say:', max_row-1)

	for row in range(start,max_row+1):
		sayTemplate(row)

print('Loading Excel')
wb = load_workbook('{}.xlsx'.format(level_type))
sheet = wb[level]
max_row = sheet.max_row

#sayRandom(60)
sayAll()