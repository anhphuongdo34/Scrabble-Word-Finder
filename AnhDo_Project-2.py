
# Anh Do - CSC 184A
# Jan 23, 2021
# Project 2: Scrabble Word Finder

from itertools import permutations
from itertools import combinations
from string import ascii_uppercase
import sys
import csv
import time

#--Global variables--#
LETTERS = []
BOARD = []
RESULTS = {}       # RESULTS = {score : [words]}
DICT = []          # contents of the scrabble_dict.txt file
LETTERS_VALUE = {}

#-------files--------#
DICT_NAME = 'scrabble_dict.txt'
LETTER_NAME = 'letter_score.csv'

#------functions-----#
#importing files and save the data for later usage
def import_dict(file) :
    global DICT
    contents = file.readlines()
    for line in contents :
        DICT.append(line.strip().lower())

def import_score(file) :
    global LETTERS_VALUE
    reader = csv.reader(file)
    header_row = next(reader)

    for row in reader :
        LETTERS_VALUE.setdefault(row[0].lower(), int(row[2]))

#greeting and introducing the user to the program
def print_greetings() :
    print('Welcome ! This program will help you playing the scrabble game.')
    print('From the letters in your tray, it will generate all the possible words')
    print('     and print the results in the order from highest to lowest score.')
    print('Let begin !')

#taking in the user's inputs and adding each letter (with repetitions)
#   to a list for later usage.
def get_letters() :
    global LETTERS
    LETTERS.clear()

    letter = '@'     #took around 12s
    print("enter the letters. '?' for blank, 2 max. empty input to finish.")
    while letter != '' and LETTERS.count('?') < 3:
        letter = input()
        letter = letter.strip()
        letter = letter.replace(' ', '')
        letter = letter.replace('\n', '')
        for char in letter :
            LETTERS.append(char.lower())

    if LETTERS.count('?') > 2 :
        print('you can only have a maximum of 2 blank tiles. please enter the letters again.')
        get_letters()

# get the board configuration for difficult position and help player
#   with words that fit in those position perfectly (i hope)
def get_board() :
    global BOARD
    BOARD.clear()

    print('enter the specific position you want to put words in.')
    print("enter letters and underscore characters '_' for blank spaces")
    pos = '@'
    while pos != '' :
        pos = input()
        BOARD.append(pos.lower())


#find all the possible words from the given letters
def word_finder() :
    global RESULTS
    global LETTERS

    blanks = LETTERS.count('?')
    letters = []
    tiles_value = tiles_score()

    for l in LETTERS :
        if l != '?' :
            letters.append(l)

    if blanks == 0 :
        word_finder_helper(letters, tiles_value)
    elif blanks == 1 :
        for char in ascii_uppercase :
            letters.append(char)
            word_finder_helper(letters, tiles_value)
            letters.pop(len(letters) - 1)
    else :
        for char1 in ascii_uppercase :
            letters.append(char1)
            for char2 in ascii_uppercase :
                letters.append(char2)
                word_finder_helper(letters, tiles_value)
                letters.pop(len(letters) - 1)
            letters.pop(len(letters) - 1)

#def word_finder_board() :


# using permutations and dictionary to find the possible words from a
#   given set of letters. calculate the score of each word and add to
#   the RESULTS
#   no_perm is used when the program need to generate possible words
#   with exact number of letters (for board configuration)
def word_finder_helper(letters, tiles_value) :
    global RESULTS
    perms = []

    # if no_perm == 'all' :
    for i in range (2, len(letters) + 1) :
        perms += list(permutations(letters, i))
    # else :
    #     perms += list(permutations(letters, no_perm)

    for perm in perms :
        for word in DICT :
            if ''.join(perm).lower() == word :
                the_word = ''.join(perm)
                score = word_score(the_word, tiles_value)
                RESULTS.setdefault(score, set())
                RESULTS[score].add(the_word)

#get the score for each tile in the given tray to save time when calculating
#   words' score by iterating through a much shorter list than the whole alphabet
def tiles_score() :
    global LETTERS
    tiles_value = {}
    for char in LETTERS :
        for letter in LETTERS_VALUE.keys() :
            if char == letter :
                tiles_value.setdefault(char, LETTERS_VALUE[letter])

    return tiles_value

#calculate the value of the word found
def word_score(word, tiles_value) :
    score = 0
    for char in word :
        for tile in tiles_value.keys() :
            if char == tile :               #uppercase letters will not get any score added
                score += tiles_value[tile]

    return score

#print the possible words list
def print_results() :
    global RESULTS

    scores_list = list(RESULTS.keys())
    scores_list.sort(reverse=True)

    print('words suggestions in the order of highest to lowest score')
    print('the blank tile is represented as an uppercase letter')
    for score in scores_list :
        print(str(score) + ':')
        print(RESULTS[score])

#-------main()-------#
try :
    dict_file = open(DICT_NAME)
    score_file = open(LETTER_NAME)
except FileNotFoundError :
    print('the files are missing')
    sys.exit()

import_dict(dict_file)
import_score(score_file)
print_greetings()
get_letters()

# print('do you want to enter a board configuration for more specific suggestions ?')
# print("enter 'y' for yes, any keys for no")
# do = input()

# if do.lower() == 'y' :
#     get_board()
#     print('entries received. processing...')
#     word_finder_board()
# else :
start = time.time()
word_finder()
end = time.time()
print_results()

print(end - start)
