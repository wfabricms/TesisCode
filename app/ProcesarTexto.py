#-*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
import treetaggerwrapper
import unicodedata
from urllib import quote_plus

class ProcesarTexto():
	def validateTextLenguage(self, text):
		# Lista de idiomas disponibles en la nltk
  		#languages = ["spanish","english","dutch","finnish","german","italian","portuguese","turkish","danish","french","hungarian","norwegian","russian","swedish"]
  		languages = ["english"]
		# Texto a analizar
		text = "Texto a analizar y del cual detectar el idioma en el que se encuentra"
 		# Dividimos el texto de entrada en tokens o palabras unicas
 		tokens = nltk.tokenize.word_tokenize(text)
 		tokens = [t.strip().lower() for t in tokens] # Convierte todos los textos a minusculas para su posterior comparacion
		# Creamos un dict donde almacenaremos la cuenta de las stopwords para cada idioma
 		lang_count = {}
		# Por cada idioma
		for lang in languages:
			stop_words = unicode(nltk.corpus.stopwords.words(lang))
     		lang_count[lang] = 0 # Inicializa a 0 el contador para cada idioma
     		# Recorremos las palabras del texto a analizar
		for word in tokens:
			if word in stop_words: # Si la palabra se encuentra entre las stopwords, incrementa el contador
				lang_count[lang] += 1
		# Obtiene el idioma con el numero mayor de coincidencias
 		detected_language = max(lang_count, key=lang_count.get) 
 		print detected_language
 		return detected_language

 	def validateTextCharacter(self, text):
 		text.replace("\"","")
 		#text.replace('”','"');
 		return text


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
	    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='/home/fabricio/python/ServerTesis/ProcessText/app/TreeTagger')
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

	def tokenizarTreeTagger(self, sentence): 
	    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='/home/fabricio/python/ServerTesis/ProcessText/app/TreeTagger')
	    tags = tagger.TagText(sentence)
	    tokens = []
	    for tag in tags:
	        #tokentag.append(tag.split())
	        tokens.append(tag.split()[0])		
	    return tokens

	def AplicarChunker(self, sentenciaTageada):
		grammar = r"""
		    ENT:
		        {<NP.*|JJ>*<NP.*>}  
		        
		    ENTCOMP:
		        {<ENT><IN><ENT>}
		        {<ENT>+<NN.>+}	
		    SUST:
		    	{<NN.*|JJ>*<NN.*>}
		    	{<NN.*>}	    	
		"""
		chunker = nltk.RegexpParser(grammar) 
		treeChunk = chunker.parse(sentenciaTageada)
		return treeChunk
		