import sys
from wordle import Wordle
from strategy import Strategy, SmolBrain

word_file = sys.argv[1] if len(sys.argv) > 1 else "wordle-answers-alphabetical.txt"
with open(word_file) as f:
  possible_words = [word.strip() for word in f.readlines()]

size = 5
wordle = Wordle(possible_words, size)
strategy = SmolBrain(wordle)

while len(strategy.wordle.possible_words) != 1:
  suggestion = strategy.suggestion()
  print(f"Suggested guess is: {suggestion.upper()}")
  result = input(f"What was the result for {suggestion.upper()}?\n")
  if result.lower() == "q" or result == "1" * size:
    sys.exit()
  strategy.wordle.update(suggestion, result)

print(f"Only remaining word is: {strategy.suggestion()}")