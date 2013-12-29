#! /usr/bin/env python
from optparse import OptionParser
from linguistic import LinguisticChains

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

  dictionary = options.dict_file
  word = options.starting_word if options.starting_word else None

  if not dictionary:
    parser.error('Please supply a dictionary file.')

  lc = LinguisticChains(words_from_file(dictionary))

  print_chains(lc.longest_chains(word))