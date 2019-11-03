# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    match_counter = 0
    for letter in letters_guessed:
      if letter in secret_word:
        match_counter += 1

    return match_counter == len(secret_word)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_word_cpy = secret_word[:]
    for char in secret_word:
      if char not in letters_guessed:
        secret_word_cpy = secret_word_cpy.replace(char, "_ ")

    return secret_word_cpy


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    import string
    avail_letters = string.ascii_lowercase

    for char in letters_guessed:
      avail_letters = avail_letters.replace(char, "")

    return avail_letters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    letters_guessed = []

    print("Welcome to the game Hangman!")
    print(f"I'm thinking of a word that is {len(secret_word)} letters long.")
    print("-------------")

    chances = 6
    warnings = 3

    vowels = "aeiou"
    consonants = string.ascii_lowercase
    for char in vowels:
      if char in consonants:
        consonants = consonants.replace(char, "")

    import re, sys  
    while True: 
      if chances != 0 and not re.search("_ ", get_guessed_word(secret_word, letters_guessed)):
        print(f"Congratulations, you won!\nYour total score for this game is: {chances * len(set(secret_word))}")
        sys.exit(0)
      elif chances == 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
        sys.exit(0)

      avail_letters = get_available_letters(letters_guessed)

      print(f"You have {chances} guesses left.")
      print(f"Available letters left: {avail_letters}.")

      letter = input("Please guess a letter: ")
      letter = letter.lower()

      if not letter.isalpha() or len(letter) != 1:
        if warnings == 0:
          chances -= 1
        else:
          warnings -= 1
          print(f"Oops! That is not a valid letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}")

      elif letter in letters_guessed:
        if warnings == 0:
          chances -= 1
        else:
          warnings -= 1
          print(f"Oops! You've already guessed that letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}") 

      elif not letter in secret_word:
        print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")  
        if letter in vowels and not letter in letters_guessed:
          chances -= 2
        elif letter in consonants and not letter in letters_guessed:
          chances -= 1

      else:
        letters_guessed.append(letter)
        print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")

      print("-------------")
      


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word:
     string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(" ", "")
    letters = 0
    accurate_letters = 0

    for char in my_word:
      if char != "_":
        letters += 1
        if char in other_word:
          accurate_letters += 1
    
    return letters == accurate_letters
        



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    print("Possible word matches are:")
    for word in wordlist:
      if match_with_gaps(my_word, word):
        print(word, end=" ")
    
    


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    letters_guessed = []

    print("Welcome to the game Hangman!")
    print(f"I'm thinking of a word that is {len(secret_word)} letters long.")
    print("-------------")

    chances = 6
    warnings = 3

    vowels = "aeiou"
    consonants = string.ascii_lowercase
    for char in vowels:
      if char in consonants:
        consonants = consonants.replace(char, "")

    import re, sys  
    while True: 
      if chances != 0 and not re.search("_ ", get_guessed_word(secret_word, letters_guessed)):
        print(f"Congratulations, you won!\nYour total score for this game is: {chances * len(set(secret_word))}")
        sys.exit(0)
      elif chances == 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
        sys.exit(0)

      avail_letters = get_available_letters(letters_guessed)

      print(f"You have {chances} guesses left.")
      print(f"Available letters left: {avail_letters}.")

      letter = input("Please guess a letter: ")
      letter = letter.lower()

      if not letter.isalpha() or len(letter) != 1:
        if letter == "*":
          show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        elif warnings == 0:
          chances -= 1
        else:
          warnings -= 1
          print(f"Oops! That is not a valid letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      
      elif letter in letters_guessed:
        if warnings == 0:
          chances -= 1
        else:
          warnings -= 1
          print(f"Oops! You've already guessed that letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}") 

      elif not letter in secret_word:
        print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")  
        if letter in vowels and not letter in letters_guessed:
          chances -= 2
        elif letter in consonants and not letter in letters_guessed:
          chances -= 1

      else:
        letters_guessed.append(letter)
        print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")

      print("-------------")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
