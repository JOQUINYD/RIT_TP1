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

    # removes tags
    # removes accents
    # convert to lowercase
    def normalize(self, text):
        onlyText = self.removeTags(text)
        accepted_accents = {u'\N{COMBINING TILDE}',}
        return ''.join(c for c in unicodedata.normalize('NFKD', onlyText) 
                        if unicodedata.category(c) != 'Mn' or c in accepted_accents).lower()    


    def splitToAcceptedWords(self,text):
        # filter out empty words
        return [word for word in re.split("\W+", text) if word not in self.stopwords]  

    def wordCount(self, fname):
        try:
            with open(fname, encoding='utf-8') as f:
                    normalizedText = self.normalize(f.read())
                    return Counter(self.splitToAcceptedWords(normalizedText))
        except:
            #if not utf-8 text file
            with open(fname) as f:
                    normalizedText = self.normalize(f.read())
                    return Counter(self.splitToAcceptedWords(normalizedText))   

    def wordCountText(self, text, stopwords):
        self.stopwords = stopwords
        normalizedText = self.normalize(text)
        return Counter(self.splitToAcceptedWords(normalizedText))
#parser = XMLParser(["para","mas","el","sus","al","de"])
#print(parser.wordCount(r"D:\joaqu\Documents\GitHub\RIT_TP1\xml-es\apx-authors.xml"))