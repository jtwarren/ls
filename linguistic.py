from memo import memoized

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