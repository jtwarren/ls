# LearnSprout coding challenge
## Part 1
Last summer my friend Vishnu, a medical student at UCSD, decided to learn programming like many others his age. He wanted to learn programming to broaden his horizons and bring his own ideas to life through apps and websites. Excited by his new intellectual venture, Vishnu tried using a variety of different resources - CodeAcademy, One Month Rails, Khan Academy, and many others. However, none of them worked. Time and again, he would get stuck, and frustrated as he tried to parse through challenging new material without any help from others. Unlike how he learned throughout his life, this time he didn't have anyone to answer his questions, point him to the right resources, and check his understanding. In seeing this, I realized that Vishnu is representative of a large group of people who don't learn best on their own and are being left behind by online education. He, like so many of us, thrives when he has someone there to help him understand the beauty and the intuition behind what it is he is learning. Learning alone, with no one there to communicate with, is unnatural, difficult, and ineffective for him.

LearnTo's solution to the problem is simple and elegant: we connect people who are interested in learning a topic with people in the same area who are passionate about sharing their knowledge on that topic. In connecting people who want to learn and share, LearnTo recreates the physical, in person, learning experience that all of us have grown up with. As such, it provides much needed support to the scores of people who want to learn new things and aren't effective at simply learning on their own. 

I am particularly proud of working on LearnTo (http://www.learnto.com/). I began working on this project with my friend, Dhruv. We came into this past semester with an idea (and a domain name :P), discussed many approaches, and built a website in around 4 days. We launched our website in November and within just one month we had over 180 user sign ups, 100 lesson requests, and 70 lessons happen or scheduled to happen.  Additionally, we have partnered with 4 coffee shops in the Cambridge area and are happy to being working with them.  We were accepted into MIT's 100k Accelerate program and we are going for another huge push over January.

If you're looking for something more technical, check out my security final project on Android Progressive Authentication: http://css.csail.mit.edu/6.858/2013/projects/jtwarren-vkgdaddy-vedha-vvelaga.pdf.

## Part 2
The major piece of this part lives in the LinguisticChains class of the linguistic.py file.  This class takes in a collection (set, list, etc) of words and allows for data about the set to be retreived. For steps 1 and 2, I have included a script for running from the command line.  The usage is below.

``` console
Usage: learn_sprout.py [options]

Options:
  -h, --help            show this help message and exit
  -d FILE, --dict=FILE  Dictionary file containing valid words.
  -w WORD, --word=WORD  Word to derive linguistic chain from.

$ ./learn_sprout.py --dict=words  --word=gnostology
gnostology => nostology => nosology => noology => oology => ology => logy => loy => ly => y
gnostology => nostology => nosology => noology => oology => ology => logy => loy => ly => l
...
gnostology => nostology => nosology => noology => oology => ology => logy => log => lo => o
gnostology => nostology => nosology => noology => oology => ology => logy => log => lo => l
```

### Approach
I initially approached this problem, and sorting jumped to mind.  If I knew that I have already processed smaller words than the given word, then I could just built the chain with a simple check of the subwords (each word made by removing a single letter).  This approached seemed okay, but I was worried about the sorting runtime.  I then thought, I could just recurse on the subwords (only valid subwords, of course), and built a chain for each word.  While a naieve attempt at this would prove catestrophic runtime, a simple memoized version runs pretty well.

### Description
The LinguisticChains class accepts a set of words, a point of concern from a memory standpoint.  In order to find the longest chain, the class will iterate over all words and keep record of the chain length as it goes (additionally storing the longest chains seen).  Each word is looked at, broken into valid subwords, added to the chains of each subword, and returned.  I initially implemented my own memoization dictionary, but decided to use the python memoization decorator for my final submission.

### Runtime
There are several pieces of the program to look at when considering runtime performance.  First, reading in the file has a O(n) runtime and memory cost.  Iterating over all of the words also has an O(n) runtime.  Recursing on each word has a k! runtime, where k is the length of the word.  This results in a O(n*k!) runtime.  However, memoizing the result of each computation means that we hit O(n) in worst case: All subwords being checked are valid and their result is only computer once.

The runtime for computing a single word still involves reading in the set of words.  This is a fixed cost though, and only happens once per instantiation of the class.  At that point, the worst case runtime is then O(k!) where k is the number of letters in the word.  This is worst case, assuming every subword of every subword and the word iteself is a valid word.

### Assumptions and optimizations



<!-- ### Step 3
For this part of the challenge, I wrote a Flask API.  I have never written an API in Flask before.  A call to `/linguistic_chains` expects a parameter `word`.  If this is missing, an HTTP status of 400 is returned.  The API will return JSON for the word given if any chains are found.  The dictionary used by the API is the words list found at `/usr/share/dict/words` on unix machines.

Example url: `http://localhost:5000/linguistic_chains?word=learning`

Example output
``` json
{"learning": [["learning", "earning", "earing"]]}
``` -->