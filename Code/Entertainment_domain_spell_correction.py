from collections import defaultdict,Counter
import re

def MyDict():
    """
    Recursive Dictionary
    """
    return defaultdict(MyDict)

class Trie:
    """
    Trie Data Structure to store the words from the dicctionary.
    """
    alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    
    def __init__(self):
        self.data = defaultdict(MyDict)

    def load(self, filename='dictionary.txt'):
        """
        Loads the dictionary words from the text file.
        """
        with open(filename, 'r') as words:
            for word in words.readlines():
                flaga=1
                for cha in word.strip():
                    if cha not in self.alphabet:
                        flaga=0
                        break 
                if flaga == 1:
                    self.add_word(word.strip())
        
    def add_word(self, word):
        """
        Function to add word in dictionary
        """
        data = self.data
        for ch in word:
            data = data[ch]
        data['$'] = True

    def find(self, word, matched=None, data=None, count=2, matches=None):
        """
        Recursive Function to find the candidate set for the query word.
        """
        if matches is None:
            matches = set()
        data = data or self.data
        matched = matched or ''

        # standard matching
        if count == 0:
            if self._search(data, word):
                matches.add(matched + word)
            return
        
        if len(word) == 0:
            if self._search(data, word):
                matches.add(matched + word)
            
            # if count > 0:
                # for ch in self.alphabet:
                #     if self._search(data, word + ch):
                #         matches.add(matched + ch)
            return

        # replaced
        _, word2 = word[0], word[1:]
        for ch in self.alphabet:
            if ch not in data:
                continue
            if ch == word[0]:
                self.find(word2, matched+ch, data[ch], count=count,matches=matches)
            else:
                self.find(word2, matched+ch, data[ch], count=count-1,matches=matches)
        
        # missing character
        word2 = word[0] + word[1:]
        for ch in self.alphabet:
            if ch not in data:
                continue
            self.find(word2, matched+ch, data[ch], count=count-1,matches=matches)
        
        # extra character 
        if len(word) >= 1:
            _, word2 = word[0], word2[1:]
            self.find(word2, matched, data, count=count-1,matches=matches)

        # transposition
        if len(word) >= 2:
            a,b,word2 = word[0],word[1],word[2:]
            self.find(a+word2,matched+b,data[b],count=count-1,matches=matches)

        return matches

    def _search(self, data, word):
        """
        Function to check if the given word is present in dictionary or not.
        """
        if not word:
            return data['$'] or False
            
        ch, word2 = word[0], word[1:]

        if ch not in data:
            return False

        return self._search(data[ch], word2)

def words(text): return re.findall(r'\w+', text.lower())

WORDS = dict(Counter(words(open('dictionary.txt').read())))


def priorProbability(word, N=100):
    """
    Probability which depicts collection frequency
    """
    return WORDS.get(word,0.1) / N+0.1 

def lcs(X, Y, m, n):
    """
    Returns length of longest common subsequence
    """  
    if m == 0 or n == 0: 
       return 0 
    elif X[m-1] == Y[n-1]: 
       return 1 + lcs(X, Y, m-1, n-1) 
    else: 
       return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n)) 

def channelModel(word,candidate):
    """
    Returns probabilty with respect to error
    """ 
    return lcs(word,candidate,len(word),len(candidate))/len(candidate) 

#def BestCandidate(candidates):
def correction(word):
    """
    Returns the most suitable candidate
    """  
    return max(t.find(word,count=1), key=lambda x:priorProbability(x)*channelModel(word,x))

if __name__ == "__main__":
    """
    Main Function takes in the query word by word and displays corrected spelling of each word.
    Count is edit distance. 
    """
    t = Trie()
    t.load()
    query = input("Enter Query: ").lower()
    for word in query.split():
        try:
            if t._search(t.data,word):
                print(f"{word} is already spelled correct.")
                continue

            print("\nCandidate set of "+word)
            print(t.find(word,count=1))
            print("\nMost Suitable Candidate is",correction(word))
        except:
            print("No suitable Correction Found.")
        
    