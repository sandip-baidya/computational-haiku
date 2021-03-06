#!/usr/bin/python
import numpy as np
import h5py
import pickle
from utils import *
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.optimizers import RMSprop

# inspiration taken from https://medium.com/@ivanliljeqvist/using-ai-to-generate-lyrics-5aba7950903
# however, we did change the model presented in that article and also the parameters. 
MODEL = 'model'
# sequence_length is number of words in the sentence beforehand
sequence_length = 1
sequence_step = 1
num_epochs = 25

def train_model(sequence_length,words,X,y):
	# Parameters and training for the model
	model = Sequential()
	model.add(LSTM(512, input_shape=(sequence_length, len(words))))
	model.add(Dense(len(words)))
	model.add(Dropout(0.7))
	model.add(Activation('softmax'))
	optimizer = RMSprop(lr=0.05)
	model.compile(loss='categorical_crossentropy', optimizer=optimizer)
	# fitting and saving the model
	history = model.fit(X, y, batch_size=1024, epochs=num_epochs,validation_split=.2)
	# saves our loss for plotting. 
	with open('loss.pickle','wb') as l:
		pickle.dump(history.history['loss'],l,protocol=pickle.HIGHEST_PROTOCOL)
	with open('val_loss.pickle','wb') as vl:
		pickle.dump(history.history['val_loss'],vl,protocol=pickle.HIGHEST_PROTOCOL)
	model.save(MODEL)


def process_data(sequences,next_words,words):
	X = np.zeros((len(sequences), sequence_length, len(words)), dtype=np.bool)
	y = np.zeros((len(sequences), len(words)), dtype=np.bool)
	for i, sequence in enumerate(sequences):
	    y[i, words.index(next_words[i])] = 1
	    for t, word in enumerate(sequence):
	        X[i, t, words.index(word)] = 1
	return X,y

def main():
	# getting and processing the data
	print('reading in data...')
	data, _ = get_train_data('haiku_2.csv')
	print('data read in!')
	#words is a sorted list of the words that appear in the data. 
	words = sorted(list(set(data.split())))
	data = data[:3*len(data)//4]
	print('generating training examples...')
	sequences, next_words = create_sequences(data, sequence_length, sequence_step)
	# converting data into arrays
	X,y = process_data(sequences,next_words,words)
	print('training examples generated!')
	print('training model...')
	model = train_model(sequence_length,words,X,y)
	print('model trained! use python3 rnn_generate.py [num_poems] to create poems')

if __name__ == '__main__':
	main()