#! /usr/bin/env python

from optparse import OptionParser
from memo import memoized

"""
Approach:
I initially approached this problem and thought about sorting
all of the words by length.  This allowed me to look at each word, and know that
I've already seen any previous words.  I could map a length and previous word to
each word that I see.  Keeping track of the longest word, I'd be able to
reconstruct the chain at the end.  I decided that this approach wasn't going to
be optimal, and thought what I could do to improve the O(nlogn) sorting.


Description:
I load all words into memory, into a set.  Then, I look at each word and check
the "subwords" of that word (subwords being those that are made by removing a
single letter).  If the subword exists in the set of words, it is a valid
precursor in the chain.  Recurse on the subword.  This could have terrible
performance but is made very efficient with memoization.  Initially I wrote my
own memoization (dict to hold the results), but decided the python decorator was
cleaner.


Runtime:
The steps, at a high level are as follows: Read in each word, check each word,
recurse on subwords.  Since the recursion is being memoized, we are doing work
for each word a maximum or 1 time.  Thus, the overall perforance runtime is
O(n).

Correctness: 
Every word is checked, and all possible subwords are checked.  The
chain is built from the top down so if a word has a valid chain, it will be
discovered. Finding the longest chain from a set of valid chains is trivial.
Thus, we are finding the longest valid linguistic chain.

"""

class LinguisticChains:

  def __init__(self, words):
    self.words = words

  """Get all subwords for a given `word`."""
  def subwords_from_word(self, word):
    return [word[:i] + word[i+1:] for i in xrange(len(word))]

  """Get all chains for a given `word`."""
  @memoized
  def chains_from_word(self, word):

    # Get all valid subwords
    subwords = [subword for subword in self.subwords_from_word(word) if subword in self.words]

    # Without valid subwords, return single `word`.
    if not subwords:
      return [(word,)]

    # Keep track of all chains
    chains = []

    # Check each valid subword
    for subword in subwords:

      # Get all chains from subword
      res = self.chains_from_word(subword)

      # Add `word` to each chain and append to chains
      for chain in res:
        chains.append((word,) + chain)

    # Return all chains of `word`
    return chains

  """Get the longest chains

  Returns: Longest chain for a given ``word`` if defined, longest chain in ``words`` otherwise.
  """
  def longest_chains(self, word=None):
    # Keep track of longest as going through words
    longest = 0
    long_chains = []

    if word:
      chains = self.chains_from_word(word)

      # Check each chain for a given word
      for chain in chains:
        length = len(chain)

        # Reset longest chain information
        if length > longest:
          long_chains = [chain]
          longest = length

        # Add to longest chain information
        elif length == longest:
          long_chains.append(chain) 
      return long_chains

    # Go through each word
    for word in self.words:
      chains = self.chains_from_word(word)

      # Check each chain for a given word
      for chain in chains:
        length = len(chain)

        # Reset longest chain information
        if length > longest:
          long_chains = [chain]
          longest = length

        # Add to longest chain information
        elif length == longest:
          long_chains.append(chain)

    return long_chains



"""Get all words from a file."""
def words_from_file(filename):
  return set(line.strip() for line in open(filename))

"""Print chains, one per line, words seperated by `=>`."""
def print_chains(chains):
  print '\n'.join(" => ".join(chain) for chain in chains)

if __name__=="__main__":
  parser = OptionParser()
  parser.add_option("-d", "--dict", dest="dict_file", help="Dictionary file containing valid words.", metavar="FILE")
  parser.add_option("-w", "--word", dest="starting_word", help="Word to derive linguistic chain from.", metavar="WORD")
  
  (options, args) = parser.parse_args()

  if not options.dict_file:
    parser.error('Please supply a dictionary file.')

  # Set containing all words from file
  words = words_from_file(options.dict_file)

  lc = LinguisticChains(words)

  # Redundant but for clarity
  starting_word = options.starting_word if options.starting_word else None

  print_chains(lc.longest_chains(starting_word))




  # # Get the longest chains
  # chains = longest_chains(words, starting_word)

  # # Print the chains
  # print_chains(chains)
