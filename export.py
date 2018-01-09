from openpyxl import *
import sys, os
from random import randint
from time import sleep
from pydub import AudioSegment
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
	sys.stdout.buffer.write((str(text) + '\n').encode('utf8'))

def sayExport(sentence, speaker, output):
	os.system('say -v {} -o {} --data-format=LEF32@22050 "{}"'.format(speaker, output, sentence))
	#os.system('say -v {} -o {} "{}"'.format(speaker, output, sentence))
	#pass

def sayTemplate(row):
	global sheet, level_type, max_row, speaker, lang, en_col, lang_col

	en_sen = sheet[en_col + str(row)].value
	if en_sen == None:
		return
	jp_sen = sheet[lang_col + str(row)].value
	print()
	print('Exporting row:', row, 'of', max_row)

	en_sen = BeautifulSoup(str(en_sen), 'lxml').text
	printText(en_sen)
	sayExport(en_sen, 'alex', 'temp/{}-{:04d}en.wav'.format(level, row))

	jp_sen = BeautifulSoup(jp_sen, 'lxml').text
	printText(jp_sen)
	sayExport(jp_sen, speaker, 'temp/{}-{:04d}{}.wav'.format(level, row, lang))

def sayAll():
	global max_row

	print('Number of sentences to say:', max_row-1)

	for row in range(2,max_row+1):
		sayTemplate(row)

def sayRandom(num_sen):
	global max_row

	print('Number of sentences to say:', num_sen)

	for i in range(num_sen):
		row = randint(2,max_row)
		sayTemplate(row)

def connectSentences(start=2, end=9999):
	global max_row, lang
	output = AudioSegment.empty()

	print('Number of sentences to merge:', max_row-1)

	for row in range(start,end+1):
		en_file = 'temp/{}-{:04d}en.wav'.format(level, row)
		if(not os.path.isfile(en_file)):
			#print('No en file')
			continue
		lang_file = 'temp/{}-{:04d}{}.wav'.format(level, row, lang)
		print()
		print('Reading row:', row, 'of', max_row)
		print(en_file)
		print(lang_file)
		output += AudioSegment.from_wav(en_file)
		output += AudioSegment.silent(duration=2000) #in milliseconds
		output += AudioSegment.from_wav(lang_file)
		output += AudioSegment.silent(duration=1000)

	return output

print('Loading Excel')
wb = load_workbook('{}.xlsx'.format(level_type))
sheet = wb[level]
max_row = sheet.max_row

sayAll()

#output = connectSentences()
#output.export('{}-{}.mp3'.format(level_type, level), format='mp3')

begin = 2
finish = max_row
number_of_chunk = 10
batch = (finish-begin)//number_of_chunk + 1

for i in range(number_of_chunk):
	start = 2+i*batch
	end = 1+(i+1)*batch
	output = connectSentences(start,end)
	output.export('{}-{}{:04d}-{:04d}.mp3'.format(level_type, level, start, end), format='mp3')

'''
begin = 5
finish = number_of_chunk

output = AudioSegment.empty()
for i in range(begin,finish):
	start = 2+i*batch
	end = 1+(i+1)*batch
	print('Appending batch', i)
	output += AudioSegment.from_mp3('{}-{}{:04d}-{:04d}.mp3'.format(level_type, level, start, end))

print('Outputting')
output.export('{}-{}-{:d}.mp3'.format(level_type, level, 2+5*batch), format='mp3')
'''
