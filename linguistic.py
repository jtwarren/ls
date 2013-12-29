from memo import memoized

def subwords_from_word(word):
  """Get the subwords for a given `word`.

  Args:
    word (str): The word for which subwords are desired.

  Returns:
    list: Subwords of the given word.  
  """
  return [word[:i] + word[i+1:] for i in xrange(len(word))]

class LinguisticChains:

  def __init__(self, words):
    self.words = words

  @memoized
  def chains(self, word):
    """Get chains for a given word.

    A chain is made by removing a single letter from a word, such that the new
    word is also a valid word.

    Args:
      word (str): The word for which chains are desired.

    Returns:
      list: Chains for the given word.  
  """
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

  def longest_chains(self, word=None):
    """Get the longest chains for a given word if supplied, otherwise the
    longest chain from the supplied words to the class will be given.

    A chain is made by removing a single letter from a word, such that the new
    word is also a valid word.

    Args:
      word (str, optional): The word for which chains are desired.

    Returns:
      list: Longest chains for the given word if supplied.  Otherwise, the
      longest chains for the supplied words to the class will be returned.
    """
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