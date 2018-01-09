import wave, struct, os
from pydub import AudioSegment

FPS = 22050

def silence(sec, output):
	global FPS

	values = []

	for i in range(0, sec*FPS):
	        value = 0
	        packed_value = struct.pack('h', value)
	        values.append(packed_value)
	        values.append(packed_value)

	value_str = b''.join(values)
	output.writeframes(value_str)

def sumAudio(infiles, outfile):
	data= []
	for infile in infiles:
		print(infile)
		w = wave.open(infile, 'rb')
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()

	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	output.writeframes(data[0][1])
	output.writeframes(data[1][1])
	output.close()

def connectSentences(start=2, end=9999):
	output = []
	level = 'SpoonFed'
	lang = 'cn'

	for row in range(start,end+1):
		en_file = 'temp/{}-{:04d}en.wav'.format(level, row)
		if(not os.path.isfile(en_file)):
			#print('No en file')
			continue
		lang_file = 'temp/{}-{:04d}{}.wav'.format(level, row, lang)
		print()
		print('Reading row:', row)
		print(en_file)
		print(lang_file)
		output += [ en_file ]
		output += [ 'temp/silence2.wav' ] #in milliseconds
		output += [ lang_file ]
		output += [ 'temp/silence1.wav' ]

	return output

sumAudio(connectSentences(), 'SpoonFed.wav')