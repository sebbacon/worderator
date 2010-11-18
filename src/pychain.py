import cPickle
import random
import os
import sys

splitsize = 3

DEBUG = False
CWD = "/home/gangle/whixey.com/worderator/"
def debug(msg):
  if DEBUG: 
    print msg

class Worderator:
  def __init__(self):
    try:
      datafile = open(CWD+"data.dat", "rb")
      self.chains = cPickle.load(datafile) 
    except:
      self.chains = {}
    print "available chains:", self.listChains()

  def listChains(self):
    return self.chains.keys()
 
  def buildchain(self, infile):
    datafile = open("data.dat", "wb")
    chain = {}
    starters = []
    for line in infile:
      line = line.lower().strip()
      if len(line) < splitsize + 1:
        continue
      starters.append(line[:splitsize])
      for x in range(0, len(line)-splitsize+1):
        stem = line[x:x+splitsize]
        tail = line[x+splitsize:x+splitsize+1]
        if not chain.has_key(stem):
          chain[stem] = []
        chain[stem].append(tail)
    chain_name = os.path.split(infile.name)[-1]
    self.chains[chain_name] = (starters, chain)
    cPickle.dump(self.chains, datafile)
    datafile.close()


  def pickChain(self, weighting=None):
    """
    pick a chain to use.  Weightings can be specified as a {'name':weight}
    dictionary.  otherwise the choice is english words only 
    """
    
    if weighting == None:
      weighting = {'words.txt':1}
    choices = []
    for k, v in weighting.items():
      if k in self.chains.keys():
        for x in range(0,int(v)):
          choices.append(k)
    if not len(choices):
      choices = ['words.txt']
    choice = random.choice(choices)
    debug("picked chain %s" % choice)
    return choice

  def worderate(self, length=None, weighting=None):
    starters, chain = self.chains[self.pickChain(weighting=weighting)]
    word = []
    stem = random.choice(starters)
    word.append(stem)
    ended = False
    while chain.has_key(stem):
      if length and len("".join(word)) == length:
        if '' not in chain[stem]:
          return self.worderate(length=length)
        else:
          ended = True
          break
      else:
        tail = random.choice(chain[stem])
      if not tail:
         ended = True
         break
      word.append(tail)
      stem = "".join(word)[-3:]
      starters, chain = self.chains[self.pickChain(weighting=weighting)]
    if not ended:
      return self.worderate(length=length) 
    else:
      return "".join(word)

#print f.chains.keys()

f = Worderator()

if len(sys.argv)>1:
 infile = open(sys.argv[1], "r")
 f.buildchain(infile)
if __name__ == "__main__":
  for x in range(0,101):
    print f.worderate(weighting={'words.txt':1,'rude.txt':5,'female-names':24})
