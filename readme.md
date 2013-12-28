# LearnSprout coding challenge
The LearnSprout coding challenge consists of 3 parts.  Part 1 is 'show and tell'.  I describe one of my most recent projects, LearnTo.  In part 2, I describe the linguistic chain coding challenge and command line interface.  For part 3, I describe the API interface to the linguistic chain program.  I decided to break the API into its own part for readability and isolation.

## Part 1
Last summer my friend Vishnu, a medical student at UCSD, decided to learn programming like many others his age. He wanted to learn programming to broaden his horizons and bring his own ideas to life through apps and websites. Excited by his new intellectual venture, Vishnu tried using a variety of different resources - CodeAcademy, One Month Rails, Khan Academy, and many others. However, none of them worked. Time and again, he would get stuck, and frustrated as he tried to parse through challenging new material without any help from others. Unlike how he learned throughout his life, this time he didn't have anyone to answer his questions, point him to the right resources, and check his understanding. In seeing this, I realized that Vishnu is representative of a large group of people who don't learn best on their own and are being left behind by online education. He, like so many of us, thrives when he has someone there to help him understand the beauty and the intuition behind what it is he is learning. Learning alone, with no one there to communicate with, is unnatural, difficult, and ineffective for him.

LearnTo's solution to the problem is simple and elegant: we connect people who are interested in learning a topic with people in the same area who are passionate about sharing their knowledge on that topic. In connecting people who want to learn and share, LearnTo recreates the physical, in person, learning experience that all of us have grown up with. As such, it provides much needed support to the scores of people who want to learn new things and aren't effective at simply learning on their own. 

I am particularly proud of working on LearnTo (http://www.learnto.com/). I began working on this project with my friend, Dhruv. We came into this past semester with an idea (and a domain name :P), discussed many approaches, and built a website in around 4 days. We launched our website in November and within just one month we had over 180 user sign ups, 100 lesson requests, and 70 lessons happen or scheduled to happen.  Additionally, we have partnered with 4 coffee shops in the Cambridge area and are happy to being working with them.  We were accepted into MIT's 100k Accelerate program and we are going for another huge push over January.

If you're looking for something more technical, check out my security final project on Android Progressive Authentication: http://css.csail.mit.edu/6.858/2013/projects/jtwarren-vkgdaddy-vedha-vvelaga.pdf.

## Part 2
The major piece of this part lives in the LinguisticChains class of the linguistic.py file.  This class takes in a collection (set, list, etc) of words and allows for data about the set to be retreived. For steps 1 and 2, I have included a script for running from the command line.  The usage is below.

``` console
$ ./learn_sprout.py --help
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
There are several pieces of the program to look at when considering runtime performance.  First, reading in the file has a O(n) runtime and memory cost.  Iterating over all of the words also has an O(n) runtime.  Recursing on each word has a k! runtime, where k is the length of the word.  This results in a O(n*k!) runtime.  However, memoizing the result of each computation means that we hit O(n) in worst case: All subwords being checked are valid and their result is only computed once.

The runtime for computing a single word still involves reading in the set of words.  This is a fixed cost though, and only happens once per instantiation of the class.  At that point, the worst case runtime is then O(k!) where k is the number of letters in the word.  This is worst case, assuming every subword of every subword and the word iteself is a valid word.  The more general case will result in a runtime of O(c*l) where l is the length of the longest chain and c is the number of chains of that lenght.  Consider 'gnostology' and the unix dictionary.  This results in 12 chains of length 10, seen above.

### Assumptions and optimizations
For this challenge, I made several assumptions.  First, that the entire dictionary could be loaded into memory (tested with unix dictionary with 235,886 words).  This is a reasonable assumption considering the unix dictionary, when loaded into a python set, is 8.0 Megabytes according to python's `__sizeof__` method.

There are various optimizations that I did not make.  This includes using information about the length of seen chains or other heuristics for decision making.  For example, if you have already seen a chain of length 7, there would be no need to check a word of length 5.  While this is an easy change, I decided to leave it out for readablity.

While I made these assumptions and optimizations (of lack of), I would be happy to discuss how things could be done differently in various situations where the needs are different (memory, cpu, load, cache, etc), or data is known (common queries, restricted data), or results do not need to hold 100% accuracy (rough estimates or approximations) in favor of speed.

## Part 3
For the API interface to the linguistic chain program, I wrote a flask API server.  I have never written a flask server before.  The API is set at the path 'linguistic_chains' and expects a parameter `word` to be supplied, resulting in a 400 if not supplied.  Any other parameters are ignored.  The API returns JSON for the given word for the longest chains found.  The dictionary used by the API is the standard unix dictionary found at '/usr/share/dict/words'.  Example usage and results can be found below.

I am currently not doing anything to defend against security attacks, and I do not know the flask framework well enough to argue the security; though I would love to talk about other frameworks and security in general!  As far as DDOS goes, there isn't anything set up in front of my server and I am not recording load.  The only protection I have is that there isn't much work done by the server for an incoming request.  In worst case, the attacker will force the server to cache (memoize) the results and the server's work will reduce over time.  

`http://localhost:5000/linguistic_chains?word=gnostology`
``` json
{
  "gnostology": [
    [
      "gnostology", 
      "nostology", 
      "nosology", 
      "noology", 
      "oology", 
      "ology", 
      "logy", 
      "loy", 
      "ly", 
      "y"
    ], 
    [
      "gnostology", 
      "nostology", 
      "nosology", 
      "noology", 
      "oology", 
      "ology", 
      "logy", 
      "loy", 
      "ly", 
      "l"
    ],
    ...
    [
      "gnostology", 
      "nostology", 
      "nosology", 
      "noology", 
      "oology", 
      "ology", 
      "logy", 
      "log", 
      "lo", 
      "o"
    ], 
    [
      "gnostology", 
      "nostology", 
      "nosology", 
      "noology", 
      "oology", 
      "ology", 
      "logy", 
      "log", 
      "lo", 
      "l"
    ]
  ]
}
```