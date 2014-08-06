import nltk
from nltk.corpus import stopwords
import treetaggerwrapper
import unicodedata
from urllib import quote_plus

class ProcesarTexto():
	def tokenizarSentencias(self, text):
	    return nltk.sent_tokenize(text)

	def tokenizarPalabras(self, text):
	    return nltk.word_tokenize(text)

	def etiquetar(self, text_tokens):
	    return nltk.pos_tag(text_tokens)

	def chunkerWithTag(self, text_tag):
	    return nltk.ne_chunk(text_tag)

	def chunker(self, text_tag):
	    return nltk.ne_chunk(text_tag, binary=True)

	def EliminarStopWords(self, word_list):
		filtered_words = [w for w in word_list if not w in stopwords.words('english') ]
		return filtered_words

	def EliminarVerbs(self, word_list):
		return [w.lower() for (w, t) in word_list if not 'VB' in t]

	def EtiquetarTreeTagger(self, sentence): 
	    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='/home/fabricio/TreeTagger')
	    tags = tagger.TagText(sentence)
	    
	    #print tags
	    duplaTag = []
	    for tag in tags:
	        #tokentag.append(tag.split())
	        duplaTag.append((tag.split()[0],tag.split()[1]))

		#duplaTag = [(i[0].encode('utf-8'),i[1].encode('utf-8')) for i in tokentag]
	        #for i in tokentag:
	        #	a  = i[0].encode('utf-8'), i[1].encode('utf-8')
	        #	duplaTag.append(a)
	    return duplaTag

	def AplicarChunker(self, sentenciaTageada):
		grammar = r"""
		    ENT:
		        {<NP.*|JJ>*<NP.*>}  # Nouns and Adjectives, terminated with Nouns
		    ENTCOMP:
		        {<ENT><IN><ENT>}  # Above, connected with in/of/etc...
		    SUST:
		    	{<NN.*|JJ>*<NN.*>}
		    	{<NN.*>}	    	
		"""
		chunker = nltk.RegexpParser(grammar) 
		treeChunk = chunker.parse(sentenciaTageada)
		return treeChunk
		