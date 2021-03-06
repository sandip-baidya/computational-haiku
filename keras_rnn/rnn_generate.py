#Code to generate poems. Enter with an optional argument for number of poems.

# for example, python rnn_generate.py 3 creates 3 poems

import keras.models
import random
import sys
import string
import numpy as np
from rnn_train import MODEL, sequence_length
from utils import *


def create_poem(firstlines,model,data,words):
	prevline = random.sample(firstlines,1)[0]
	poem = ''
	poem += prevline+'\n'
	print(prevline)
	prevline = prevline.split()
	prevline = prevline[-sequence_length:]
	# one index for clarity
	numlines = 1
	currline = []
	while numlines < 3:
		if numlines == 1:
			line_syllable_count = 3
		else:
			line_syllable_count = 5
		x = np.zeros((1,sequence_length, len(words)))
		for i, word in enumerate(prevline):
			x[0,i,words.index(word)] = 1
		#sample highest prob one. with some diversity
		prediction = model.predict(x,verbose=0)[0]
		next_index = sample(prediction,temperature=1)
		next_word = words[next_index]
		currline.append(next_word)
		if syllable_count(' '.join(currline)) >= line_syllable_count:
			poem += ' '.join(currline) + '\n'
			print(' '.join(currline))
			numlines += 1
			currline = []
		# loop to next word in sentence. 
		prevline.append(next_word)
		if len(prevline) > sequence_length:
			prevline = prevline[1:]
	return poem 




def main():
	num_poems = 1
	if len(sys.argv) >=2:
		num_poems = int(sys.argv[1])
	try:
		model = keras.models.load_model(MODEL)
	except OSError:
		# could not find model
		raise Exception("Please learn the model by running python3 rnn_train.py first!")
	data, firstlines = get_train_data('haiku_2.csv')
	# list of words in the data
	words = sorted(list(set(data.split())))
	open('poems.txt','w').close()
	#new test set of poems we have not seen. 
	data = data[3*len(data)//4:]
	for _ in range(num_poems):
		poem = create_poem(firstlines,model,data,words)
		with open('poems.txt','a') as f:
			f.write(poem+'\n')
		print('')


if __name__ == '__main__':
	main()