import statistics
from wordle import Wordle
from strategy import Strategy, SmolBrain

word_file = "wordle-answers-alphabetical.txt"
with open(word_file) as f:
  words = [word.strip() for word in f.readlines()]

def result_for_guess(guess, word):
  result = ["3"] * len(guess)
  yellows = {}

  # Have to assign greens first because of repeated letter BS why is it so complicated
  for pos in range(len(guess)):
    if guess[pos] == word[pos]:
      result[pos] = "1"

  word_without_green = [c for pos, c in enumerate(word) if result[pos] != "1"]
  for pos in range(len(guess)):
    if result[pos] == "1":
      continue
    if word_without_green.count(guess[pos]) - yellows.get(guess[pos], 0) > 0:
      result[pos] = "2"
      yellows[guess[pos]] = yellows.get(guess[pos], 0) + 1
    else:
      result[pos] = "3"
    
  return "".join(result)


def guesses_for_word(strategy, word, debug):
  if debug:
    print(word)
  strategy.wordle.reset()
  guesses = 0
  result = ""
  while result != "11111":
    guess = strategy.suggestion()
    result = result_for_guess(guess, word)
    if debug:
      print(result)
    guesses += 1
    strategy.wordle.update(guess, result)

  return guesses


debug = False
wordle = Wordle(words, 5)

# idk good enough for strategy registration not like ill have more than 3 lmao
strategies = [SmolBrain(wordle, debug)]

for strategy in strategies:
  print(f"Running benchmark for {strategy.__class__.__name__}")
  print(f"Strategy: {strategy.description()}")
  results = {word: guesses_for_word(strategy, word, debug) for word in words}
  max_guesses = max(results.values())
  max_guess_words = [word for word in results if results[word] == max_guesses]

  print(f"Mean guesses: {statistics.mean(results.values())}")
  print(f"Most guesses taken: {max_guesses}")
  print(f"Words taking {max_guesses} guesses:")
  print("\n".join(max_guess_words))