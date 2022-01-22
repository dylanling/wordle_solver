from abc import ABC, abstractmethod
from wordle import Wordle
 
class Strategy(ABC):
  def __init__(self, wordle, debug=False, initial_guess="roate"):
    self.wordle = wordle
    self.initial_guess = initial_guess
    self.debug = debug

  @abstractmethod
  def description(self):
    pass

  @abstractmethod
  def suggestion(self):
    pass
 
class BasicFrequency(Strategy):
  def __init__(self, wordle, debug=False, initial_guess="roate"):
    super().__init__(wordle, debug, initial_guess)
    self.frequencies = self.__build_letter_frequencies(self.wordle.possible_words)

  def description(self):
    return """Just go through original possible words, score by
    frequency (sum of letter frequency discounting dupes)
    and pick the biggest score.
    """

  def suggestion(self):
    if not self.wordle.guesses:
      return self.initial_guess

    scores = {word: sum(self.frequencies[letter] for letter in set(word)) for word in self.wordle.possible_words}
    suggestion = max(scores, key=scores.get)

    if self.debug:
      print(f"possible words: {self.wordle.possible_words}")
      print(f"possible letters: {self.wordle.possible_letters}")
      print(f"suggestion: {suggestion}")

    return suggestion

  def __build_letter_frequencies(self, possible_words):
    frequencies = {letter: 0 for letter in Wordle.ALPHABET}
    for word in possible_words:
      for letter in word:
        frequencies[letter] += 1
    return frequencies

class IteratedFrequency(Strategy):
  def __init__(self, wordle, debug=False, initial_guess="roate"):
    super().__init__(wordle, debug, initial_guess)
    self.frequencies = self.__build_letter_frequencies(self.wordle.possible_words)

  def description(self):
    return """Score by frequency (sum of letter frequency discounting dupes)
    and pick the biggest score. Frequency ranking is recomputed by current
    possible words.
    """

  def suggestion(self):
    if not self.wordle.guesses:
      return self.initial_guess

    self.frequencies = self.__build_letter_frequencies(self.wordle.possible_words)

    scores = {word: sum(self.frequencies[letter] for letter in set(word)) for word in self.wordle.possible_words}
    suggestion = max(scores, key=scores.get)

    if self.debug:
      print(f"possible words: {self.wordle.possible_words}")
      print(f"possible letters: {self.wordle.possible_letters}")
      print(f"suggestion: {suggestion}")

    return suggestion

  def __build_letter_frequencies(self, possible_words):
    frequencies = {letter: 0 for letter in Wordle.ALPHABET}
    for word in possible_words:
      for letter in word:
        frequencies[letter] += 1
    return frequencies
