#! flask/bin/python

from flask import jsonify
from flask import Flask
from flask import request
from flask import abort

from learn_sprout import LinguisticChains

app = Flask(__name__)

# Not sure how to do this, want lc to persist while server runs.
# Effect is that it caches results (longest_chains is memoized).
lc = LinguisticChains([])

@app.route('/linguistic_chains')
def linguistic_chains():

  # Get starting word from arugments
  starting_word = request.args.get('word')

  # Return 400 if not supplied
  if not starting_word:
      abort(400)

  # Get chain for starting word
  chains = lc.longest_chains(starting_word)

  # Return json of chains
  return jsonify({starting_word: chains})

if __name__ == '__main__':
  # For server, use words dictionary
  words = set(line.strip() for line in open('words'))

  # Set LinguisticChains to use words
  lc = LinguisticChains(words)

  # Run server
  app.run(debug = True)