import random
import re
import numpy as np
import math
import requests
from bs4 import BeautifulSoup
import time
import gensim
from gensim.models import word2vec
from gensim.models import KeyedVectors
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import spacy
  
nlp = spacy.load('en_core_web_sm')

# model = Word2Vec.load("./word2vecmodel")
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
opts = Options()
opts.add_argument("--log-level=3")
opts.binary_location= 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'

chrome_driver = "C:/Users/manju/Downloads/chromedriver_win32/chromedriver.exe"

driver = webdriver.Chrome(options=opts, executable_path=chrome_driver, service_log_path = 'NUL')

room_name = str(input("Enter name of the Game room: "))
URL = 'https://www.horsepaste.com/' + room_name
print(URL)
driver.get(URL)

time.sleep(5) 
  
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
# print(soup.prettify())
blue_words = soup.find_all('div', {'class': 'cell blue hidden-word'})
red_words = soup.find_all('div', {'class': 'cell red hidden-word'})
neutral_words = soup.find_all('div', {"class": 'cell neutral hidden-word'})
black_word = soup.find_all('div', {"class": 'cell black hidden-word'})

blue = []
red = []
neutral = []
black = []
all_words = []

for x in blue_words:
	blue.append(x.text)
	all_words.append(x.text)
for x in red_words:
	red.append(x.text)
	all_words.append(x.text)
for x in neutral_words:
	neutral.append(x.text)
	all_words.append(x.text)
for x in black_word:
	black.append(x.text)
	all_words.append(x.text)
print("\n")
k = 0
for i in range(5):
	for j in range(5):
		print(all_words[k], end = "  ")
		k = k + 1
	print("\n")

def print_gamescene(all_words, guess, blue, red, neutral, black):
	for i in range(len(all_words)):
		if(all_words[i] == guess):
			if guess in blue:
				all_words[i] += "(Blue)"
			elif guess in red:
				all_words[i] += "(Red)"
			elif guess in neutral:
				all_words[i] += "(Neutral)"
			elif guess in black:
				all_words[i] += "(DEAD)"
	print("\n")
	k = 0
	for i in range(5):
		for j in range(5):
			print(all_words[k], end = "  ")
			k = k + 1
		print("\n")

def similarity(w1, w2):
	words = w1 + " " + w2
	tokens = nlp(words)  
	token1, token2 = tokens[0], tokens[1]
	return token1.similarity(token2)

def AI_assistant(all_words, clue_word):
	# pass
	remaining_words = []
	for w in all_words:
		if '(' in w:
			continue
		remaining_words.append(w)
	remaining_words = sorted(remaining_words, key = lambda w: model.similarity(w, clue_word))
	print("The AI assistant's top guesses: ")
	scores = []
	for w in remaining_words:
		scores.append(model.similarity(w, clue_word))
	for i in range(6):
		if len(remaining_words) - 1 - i >= 0:
			print(remaining_words[len(remaining_words) - 1 - i], scores[len(remaining_words) - 1 - i])
	print("\n")

turn_count = 1
first = 1
blue_left = len(blue)
red_left = len(red)
game_over = False
if blue_left > red_left:
	first = 0
while blue_left > 0 and red_left > 0 and not game_over:
	if first == 0:
		print("Waiting for Blue Spymaster to give clue. Enter the word first, and number in the next line")
		clue_word = str(input())
		# clue_word = clue.split(",")[0]
		clue_num = int(input())
		print("Team Blue's clue is : ", clue_word, clue_num)
		AI_assistant(all_words, clue_word)
		print("Blue team can make their guesses")
		stop = False
		k = 0
		while(not stop):
			guess = str(input()).upper()

			if guess not in all_words:
				print("Your guess is not present in the Grid, retry")
			else:
				if guess in blue:
					print("CORRECT GUESS!!!")
					blue_left -= 1
					
					print_gamescene(all_words, guess, blue, red, neutral, black)
					print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
					k += 1
					if k == clue_num:
						print("Your turn ends here.")
						stop = True
						break
				else:
					if guess in red:
						print("OOPS! You guessed a word from RED Team, your turn ends here.")
						red_left -= 1
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in neutral:
						print("OOPS! You guessed a neutral word, your turn ends here.")
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in black:
						print("OOPS! You guessed the deadliest word. GAME OVER! RED TEAM WINS")
						print_gamescene(all_words, guess, blue, red, neutral, black)
						stop = True
						game_over = True
			

		if game_over:
			break

		print("Waiting for Red Spymaster to give clue. Enter the word first, and number in the next line")
		clue_word = str(input())
		# clue_word = clue.split(",")[0]
		clue_num = int(input())
		print("Team Red's clue is : ", clue_word, clue_num)
		AI_assistant(all_words, clue_word)
		print("Red team can make their guesses")
		stop = False
		k = 0
		while(not stop):
			guess = str(input()).upper()
			if guess not in all_words:
				print("Your guess is not present in the Grid")
			else:
				if guess in red:
					print("CORRECT GUESS!!!")
					red_left -= 1
					
					print_gamescene(all_words, guess, blue, red, neutral, black)
					print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
					k += 1
					if k == clue_num:
						print("Your turn ends here.")
						stop = True
						break
				else:
					if guess in blue:
						print("OOPS! You guessed a word from Blue Team, your turn ends here.")
						blue_left -= 1
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in neutral:
						print("OOPS! You guessed a neutral word, your turn ends here.")
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in black:
						print("OOPS! You guessed the deadliest word. GAME OVER! RED TEAM WINS")
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
						game_over = True
			
	else:
		print("Waiting for Red Spymaster to give clue. Enter the word first, and number in the next line")
		clue_word = str(input())
		# clue_word = clue.split(",")[0]
		clue_num = int(input())
		print("Team Red's clue is : ", clue_word, clue_num)
		AI_assistant(all_words, clue_word)
		print("Red team can make their guesses")
		stop = False
		k = 0
		while(not stop):
			guess = str(input()).upper()
			if guess not in all_words:
				print("Your guess is not present in the Grid")
			else:
				if guess in red:
					print("CORRECT GUESS!!!")
					red_left -= 1
					
					print_gamescene(all_words, guess, blue, red, neutral, black)
					print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
					k += 1
					if k == clue_num:
						print("Your turn ends here.")
						stop = True
						break
				else:
					if guess in blue:
						print("OOPS! You guessed a word from Blue Team, your turn ends here.")
						blue_left -= 1
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in neutral:
						print("OOPS! You guessed a neutral word, your turn ends here.")
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in black:
						print("OOPS! You guessed the deadliest word. GAME OVER! RED TEAM WINS")
						print_gamescene(all_words, guess, blue, red, neutral, black)
						stop = True
						game_over = True

		if game_over:
			break

		print("Waiting for Blue Spymaster to give clue. Enter the word first, and number in the next line")
		clue_word = str(input())
		# clue_word = clue.split(",")[0]
		clue_num = int(input())
		print("Team Blue's clue is : ", clue_word, clue_num)
		AI_assistant(all_words, clue_word)
		print("Blue team can make their guesses")
		stop = False
		k = 0
		while(not stop):
			guess = str(input()).upper()
			if guess not in all_words:
				print("Your guess is not present in the Grid, retry")
			else:
				if guess in blue:
					print("CORRECT GUESS!!!")
					blue_left -= 1
					
					print_gamescene(all_words, guess, blue, red, neutral, black)
					print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
					k += 1
					if k == clue_num:
						print("Your turn ends here.")
						stop = True
						break
				else:
					if guess in red:
						print("OOPS! You guessed a word from RED Team, your turn ends here.")
						red_left -= 1
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in neutral:
						print("OOPS! You guessed a neutral word, your turn ends here.")
						
						print_gamescene(all_words, guess, blue, red, neutral, black)
						print("Current Game state: Blue = ", blue_left, " Red = ", red_left)
						stop = True
					if guess in black:
						print("OOPS! You guessed the deadliest word. GAME OVER! RED TEAM WINS")
						print_gamescene(all_words, guess, blue, red, neutral, black)
						stop = True
						game_over = True
			




