from collections import Counter
import re
import unicodedata

class XMLParser:

    stopwords = []

    def __init__(self):
        self.stopwords = []

    def setStopwords(self, stopwords):
        self.stopwords = stopwords

    def removeTags(self, text):
        return re.sub(pattern="\<[^>]*\>", repl=" " , string=text)

    # removes accents
    # convert to lowercase
    def normalize(self, text):
        accepted_accents = {u'\N{COMBINING TILDE}',}
        return ''.join(c for c in unicodedata.normalize('NFKD', text) 
                        if unicodedata.category(c) != 'Mn' or c in accepted_accents).lower()    


    def splitToAcceptedWords(self,text):
        text = self.removeTags(text)
        allWords = self.normalize(re.sub(pattern="[\W]", repl=" " ,string=text)).split()
        acceptedWords = []
        for word in allWords:
            #word = unicode(word,"utf-8")
            if word not in self.stopwords:
                acceptedWords += [word]
        return acceptedWords

    def process(self, text):
        #To lowercase
        text = text.lower()
        # Remove accents
        trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
        text = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', text).translate(trans_tab))
        #Find valid words
        tokens = re.findall("[a-zA-Z0-9ñ_]+",text)
        #Sort the words  
        tokens = sorted(tokens)

        acceptedWords = []
        for word in tokens:
            if word not in self.stopwords:
                acceptedWords += [word]

        #Group words
        return dict(Counter(acceptedWords))

    def wordCount(self, fname):
        try:
            with open(fname, encoding='utf-8') as f:
                    return self.process(self.removeTags(f.read()))
        except:
            #if not utf-8 text file
            with open(fname) as f:
                    return self.process(self.removeTags(f.read()))  

    def wordCountText(self, text, stopwords):
        self.stopwords = stopwords
        return self.process(text)

#parser = XMLParser()
#parser.setStopwords(['a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'e', 'el', 'en', 'entre', 'hacia', 'hasta', 'ni', 'la', 'le', 'lo', 'los', 'las', 'o', 'para', 'pero', 'por', 'que', 'se', 'segun', 'sin', 'so', 'sobre', 'tras', 'u', 'un', 'una', 'unas', 'uno', 'unos', 'y'])
#print(parser.wordCount(r'D:\joaqu\Documents\GitHub\RIT_TP1\xml-es\xacc-y2k.xml'))
#with open(r'D:\joaqu\Documents\GitHub\RIT_TP1\xml-es\xacc-y2k.xml',encoding='utf-8') as f:
#    for word in parser.splitToAcceptedWords(f.read()):
#        print(word)

#print(parser.wordCount(r'D:\joaqu\Documents\GitHub\RIT_TP1\xml-es\xacc-y2k.xml'))
#print(parser.wordCount(r"D:\joaqu\Documents\GitHub\RIT_TP1\xml-es\apx-authors.xml"))