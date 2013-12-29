from memo import memoized

"""Get the subwords for a given `word`."""
def subwords_from_word(word):
  return [word[:i] + word[i+1:] for i in xrange(len(word))]

class LinguisticChains:

  def __init__(self, words):
    self.words = words

  @memoized
  def chains(self, word):

    # Get all valid subwords
    subwords = [subword for subword in subwords_from_word(word) if subword in self.words]

    # Without valid subwords, return single `word`.
    if not subwords:
      return [(word,)]

    # Keep track of all chains
    chains = []

    # Check each valid subword
    for subword in subwords:

      # Get all chains from subword
      res = self.chains(subword)

      # Add `word` to each chain and append to chains
      for chain in res:
        chains.append((word,) + chain)

    # Return all chains of `word`
    return chains

  """Get the longest chains for a given `word`.  If no word is supplied, get the longest chain from `words`"""
  def longest_chains(self, word=None):
    words = [word] if word else self.words

    # Keep track of longest as going through words
    longest = 0
    long_chains = []

    # Go through each word
    for word in words:
      chains = self.chains(word)

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