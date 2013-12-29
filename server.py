#! flask/bin/python

from flask import jsonify
from flask import Flask
from flask import request
from flask import abort

from learn_sprout import LinguisticChains

app = Flask(__name__)

words = set(line.strip() for line in open('words'))

lc = LinguisticChains(words)

@app.route('/linguistic_chains')
def linguistic_chains():

  # Get starting word from arugments
  starting_word = request.args.get('word')

  # Return 400 if not supplied
  if not starting_word:
      abort(400)

  # Get chain for starting word
  chains = lc.longest_chains(starting_word)

  print chains

  # Return json of chains
  return jsonify({starting_word: chains})

# if __name__ == '__main__':
#   # For server, use words dictionary
#   words = set(line.strip() for line in open('words'))

#   # Set LinguisticChains to use words
#   lc = LinguisticChains(words)

#   # Run server
#   app.run(debug = True)