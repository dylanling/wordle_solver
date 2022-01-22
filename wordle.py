class Wordle:
  ALPHABET = "abcdefghijklmnopqrstuvwxyz"

  def __init__(self, possible_words, size):
    self.all_possible_words = possible_words
    self.size = size

    # List of word guesses
    self.guesses = []
    # List of results corresponding to each guess
    # A result is a string composed of the values
    # '1' (green), '2' (yellow), or '3' (gray)
    self.results = []
    self.possible_words = set(possible_words)
    self.possible_letters = {pos: set(Wordle.ALPHABET) for pos in range(self.size)}
    self.yellow_letters = set()
    self.impossible_letters = set()

  def reset(self):
    self.guesses = []
    self.results = []
    self.possible_words = set(self.all_possible_words)
    self.possible_letters = {pos: set(Wordle.ALPHABET) for pos in range(self.size)}
    self.yellow_letters = set()
    self.impossible_letters = set()

  def suggest(self):
    if not self.guesses:
      return "roate"

    # Very smol brain for now
    # Just go through possible words, score by frequency (sum of letter frequency discounting dupes)
    # and pick the biggest score.
    scores = {word: sum(self.frequencies[letter] for letter in set(word)) for word in self.possible_words}
    suggestion = max(scores, key=scores.get)

    return suggestion

  def update(self, guess, result):
    guess = guess.lower()
    self.guesses += guess
    self.results += result

    for pos, res in enumerate(result):
      if res == "1":
        self.possible_letters[pos] = {guess[pos]}
      elif res == "2":
        self.possible_letters[pos] -= {guess[pos]}
        self.yellow_letters.add(guess[pos])
      elif res == "3":
        self.__remove_possible_letter(pos, guess[pos])

    self.__update_possible_words()

  def __remove_possible_letter(self, pos, letter):
    if letter in self.yellow_letters:
      self.possible_letters[pos].remove(letter)
      return
    
    for pos in self.possible_letters:
      # slightly faster than set difference
      if len(self.possible_letters[pos]) > 1 and letter in self.possible_letters[pos]:
        self.possible_letters[pos].remove(letter)

    for pos in self.possible_letters:
      if letter in self.possible_letters[pos]:
        return # don't mark impossible if it's a green

    self.impossible_letters.add(letter)

  def __is_word_legal(self, word):
    for pos, letter in enumerate(word):
      if letter not in self.possible_letters[pos]:
        return False
    for letter in self.yellow_letters:
      if letter not in word:
        return False
    return True

  def __update_possible_words(self):
    self.possible_words = {word for word in self.possible_words if self.__is_word_legal(word)}
