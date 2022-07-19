# File : main.py
# Implementing graph.py to predict words

import os
import re
import random
import string

from graph import Graph, Vertex

def get_words_from_text(text_path):
	# Read file as bytes --> Decode UTF-8
	with open(text_path, 'rb') as file:
		text = file.read().decode('utf-8')

		# Replace [<somthing>] to blank space: "[Chorus]" --> " "
		text = re.sub(r'\[(.+)\]', ' ', text)

		text = ' '.join(text.split())
		text = text.lower()

		# Replace '' with '' and remove all punctuations
		# https://www.w3schools.com/python/ref_string_maketrans.asp
		text = text.translate(str.maketrans('', '', string.punctuation))

	words = text.split() # Get list of words
	words = words[:1000]

	return words

def make_graph(words):
	# Initialize Graph
	g = Graph()

	prev_word = None

	# For each word in words
	for word in words:
		word_vertex = g.get_vertex(word)
		if prev_word:
			prev_word.increment_edge(word_vertex)

		# Assign the current word as the previous word
		prev_word = word_vertex

	g.generate_probability_mappings()

	return g

def compose(g, words, length=50):
	composition = []

	# Pick one vertex of word
	word = g.get_vertex(random.choice(words))
	
	for _ in range(length):
		composition.append(word.value)
		word = g.get_next_word(word)

	return composition

def main():
	# words = get_words_from_text('text/hp_sorcerer_stone.txt')

	words = []

	artist = 'green_day'

	for song in os.listdir(f'songs/{artist}'):
		if song == '.DS_Store':
			continue
		words.extend(get_words_from_text(f'songs/{artist}/{song}'))

	g = make_graph(words)
	composition = compose(g, words, 100)
	print(' '.join(composition))

if __name__ == '__main__':
	main()