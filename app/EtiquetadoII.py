# -*- coding: utf-8 -*-
import urllib2
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import nltk
from nltk.corpus import stopwords
import os
import treetaggerwrapper
import MySQLdb
import unicodedata
from urllib import quote_plus

def PreparaFiltroTexto(recurso):
	tittletyope = ""	
	for s in recurso.split():
		if s.lower() in stopwords.words('english') or s.lower() in stopwords.words('spanish'):
			tittletyope = tittletyope + s.lower() + ' ' 
		else:
			tittletyope = tittletyope + s.title() + ' ' 
	tittletyope = tittletyope[:-1]
	return tittletyope

def ejecutarQuery(SparqlQuery, servidor):
	sparql = SPARQLWrapper(servidor)
	sparql.setQuery(SparqlQuery)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results

def extraeListaDesdeJson(results):
	uris = []
	for result in results["results"]["bindings"]:
		if "amb1" in result.keys():
			if result["amb1"]["value"]  not in uris and "http://dbpedia.org/resource/" in result["amb1"]["value"]:  uris.append(result["amb1"]["value"])	
		elif "redir" in result.keys():
			if result["redir"]["value"] not in uris and "http://dbpedia.org/resource/" in result["redir"]["value"]: uris.append(result["redir"]["value"])	
		elif "amb" in result.keys():
			if result["amb"]["value"]   not in uris and "http://dbpedia.org/resource/" in result["amb"]["value"]:   uris.append(result["amb"]["value"])	
		else:
			if result["x"]["value"]     not in uris and "http://dbpedia.org/resource/" in result["x"]["value"]:     uris.append(result["x"]["value"])		
	return uris

def getQuery(term):
	SparqlQueryPrefix = """
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		"""
	SparqlQuery = """
		"""+SparqlQueryPrefix+"""
		SELECT distinct ?x ?amb ?redir ?amb1
		WHERE {
			?x ?predicado ?text.
			OPTIONAL { ?x dbpedia-owl:wikiPageDisambiguates ?amb }
			OPTIONAL { ?x dbpedia-owl:wikiPageRedirects ?redir }
			OPTIONAL { ?redir dbpedia-owl:wikiPageDisambiguates ?amb1 }
			FILTER (?predicado = foaf:name || ?predicado = rdfs:label)
			FILTER (?text = '"""+term+"""'@en)
		}
	""" #%(tittletyope, recurso) #%(encoded_url.lower(), encoded_url.upper(), tittletyope, encoded_url)
	return SparqlQuery

def extraerListRecursoDBpedia(recurso): #return list[] labels de un recurso
	#print "URI Recurso: ", recurso
	#print SparqlQuery
	servidor = "http://localhost:8890/sparql"
	filterText = PreparaFiltroTexto(recurso)
	if recurso == filterText:
		results = ejecutarQuery(getQuery(recurso),servidor)
	else:
		results = ejecutarQuery(getQuery(filterText),servidor)
		if len(results["results"]["bindings"]) == 0 :
			results = ejecutarQuery(getQuery(recurso),servidor)

	if len(results["results"]["bindings"]) == 0 and servidor != "http://localhost:8890/sparql":
		SparqlQuery = """
			SELECT ?x
			WHERE { ?x ?predicado ?text .
			FILTER (?predicado = foaf:name || ?predicado = rdfs:label)
			FILTER (lcase(str(?text)) = """+recurso+""") .
			}
		"""
		results = ejecutarQuery(SparqlQuery,servidor)

	if not len(results["results"]["bindings"]) == 0 :
		uris = extraeListaDesdeJson(results)
	else:
		return []
	#print uris
	recursosDbpediaAbstr = []
	for u in uris:
		#print "URI >>", u
		recDbpediaAbstr = {"uri":"", "abstract":""}
		recDbpediaAbstr["uri"] = u
		SparqlQuery = """
		    select ?abstract where {<"""+u+"""> <http://www.w3.org/2000/01/rdf-schema#comment> ?abstract. 
		    FILTER (lang (?abstract)="en")} 
		"""
		#print SparqlQuery
		sparql = SPARQLWrapper(servidor)
		sparql.setQuery(SparqlQuery)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		if len(results["results"]["bindings"]) > 0 : 
			#print "Abstract >>",results["results"]["bindings"][0]["abstract"]["value"]
			#print tokenizarSentences(results["results"]["bindings"][0]["abstract"]["value"])[0]
			abstract = ExtraerNombres(tokenizarSentences(results["results"]["bindings"][0]["abstract"]["value"])[0])
			#print  abstract
			#print "\nyyy",EliminarVerbs(etiquetar(tokenizar(tokenizarSentences(results["results"]["bindings"][0]["abstract"]["value"])[0])))
			#print "xxx", EliminarStopWords(EliminarVerbs(etiquetar(tokenizar(tokenizarSentences(results["results"]["bindings"][0]["abstract"]["value"])[0]))))
			#print recDbpediaAbstr["uri"], ">> ", abstract, "\n"
			recDbpediaAbstr["abstract"] = abstract
			#print recDbpediaAbstr["abstract"]

		else:
			#print recDbpediaAbstr["uri"]
			#print recDbpediaAbstr["uri"][len("http://dbpedia.org/resource/"):].replace('_',' ')
			recDbpediaAbstr["abstract"] = recDbpediaAbstr["uri"][len("http://dbpedia.org/resource/"):].replace('_',' ')	.split()
			#print "No ABSTRACT"

		recursosDbpediaAbstr.append(recDbpediaAbstr)
	return recursosDbpediaAbstr # return [{"uri":"", "abstract":""}, {"uri":"", "abstract":""}]
 
def ExtraerNombres(sentence):
 	ett = etiquetar(tokenizar(sentence))
	abstract = [w for (w, x) in ett if len(w)>2  and x =='NNP' or x =='NNPS' or x =='NN' or x =='NNS']
	return abstract

def EtiquetarTT(sentence): 
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
def tokenizarSentences(text):
    return nltk.sent_tokenize(text)

def tokenizar(text):
    return nltk.word_tokenize(text)

def etiquetar(text_tokens):
    return nltk.pos_tag(text_tokens)

def chunkerWithTag(text_tag):
    return nltk.ne_chunk(text_tag)

def chunker(text_tag):
    return nltk.ne_chunk(text_tag, binary=True)

def EliminarStopWords(word_list):
	filtered_words = [w for w in word_list if not w in stopwords.words('english') ]
	return filtered_words

def EliminarVerbs(word_list):
	return [w.lower() for (w, t) in word_list if not 'VB' in t]

def ExtraerData(sentence):
	ents  = []
	keys1 = []
	keys2 =[]
	print "Sentencia > ",sentence
	ett = EtiquetarTT(sentence)
	keys2 = [w for (w, x) in ett if len(w)>2  and x =='NN' or x =='NNS']
	treeChunk = chunker.parse(ett)
	#print treeChunk
	for x in treeChunk.subtrees():
		#print x
		if x.node == 'SUST':	
			word = [w[0] for w in x.leaves()]
			name = " ".join(word)
			if len(name) >2 and name not in keys2: keys1.append(name)
		if x.node == 'ENTCOMP' or x.node == 'ENT':
			word = [w[0] for w in x.leaves()]
			name = " ".join(word)
			if len(name) >2: ents.append(name)
	return [ents,keys1,keys2] # retorna [entidades[], keywordsCompuestas[], keywordsimples[]]

def CalcularConcordancia(abstract_j, abstract_l, listSentence):
	concordancia = 0
	"""
	print "1 ", abstract_j
	print "2 ",abstract_l 
	print "3 ",listSentence
	print "4 ",abstract_l  + listSentence
	print """
	
	for word_j in abstract_j:
		for word_l in abstract_l + listSentence:
			if word_l.lower() == word_j.lower(): concordancia = concordancia + 1
	return concordancia

def Desambiguacion(listData, listSentence):
	#listData = [{"label":"", "frequency":"","dbpediaResource":"","DBpedRList":[{"uri":"", "abstract":""}], "type":0}]
	for word_i in listData:
		if len(word_i['DBpedRList']) == 1 :
			word_i['dbpediaResource'] = word_i['DBpedRList'][0]['uri']
			print word_i['dbpediaResource']
			continue
		#print "\n	",word_i['label'], "..."
		BEST_SCORE = 0
		BEST_SENSE = ""
		BEST_ABSTR = ""
		for sense_j in word_i['DBpedRList']:
			SCORE = 0
			for word_k in listData:

				if word_i['label'] != word_k['label']:
					for sense_l in word_k['DBpedRList']:
						SCORE = SCORE + CalcularConcordancia(sense_j['abstract'], sense_l['abstract'], listSentence)
			if SCORE > BEST_SCORE:
				BEST_SCORE = SCORE
				BEST_SENSE = sense_j['uri']

		if BEST_SCORE > 0:
			word_i['dbpediaResource'] = BEST_SENSE
			print "SCORE", BEST_SCORE, ", ", BEST_SENSE
		else:
			print word_i,": ambiguo"
	return listData

text = """The last seven Syrian Christians in rebel-held Aleppo await the end of their lives in a pensioners’ hostel serenaded by barrel bombs, rockets and gunfire, so isolated from the reach of their church that they bury their dead in the garden.""".decode("utf-8")

grammar = r"""
    ENT:
    	
        {<NP.*|JJ>*<NP.*>}  # Nouns and Adjectives, terminated with Nouns
        
    ENTCOMP:
        {<ENT><IN><ENT>}  # Above, connected with in/of/etc...
    
    SUST:
    	{<NN.*|JJ>*<NN.*>}
    	{<NN.*>}
    	
"""
#print EliminarStopWords(tokenizar(text))
bd = MySQLdb.connect("localhost","root","root","scopus_db",charset='utf8',use_unicode=True )
tabla = 'tripleta'
# Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cursor = bd.cursor()
# Preparamos el query SQL para obtener todos los empleados de la BD 
sql = "SELECT objeto FROM  `tripleta` WHERE  `predicado` =  'abstract'"
cursor.execute(sql)
# Obtenemos todos los registros en una lista de listas
resultados = cursor.fetchall()
#resultados = ["Juan Pablo has a beutiful car"]
#print treeChunk
#fre = nltk.FreqDist(treeChunk)
data ={}
data['TotalSentences'] = 0
data['TotalEntities'] = 0
data['TotalKeywordsComp'] = 0
data['TotalKeywordsSimp'] = 0
data['entities'] = []
data['keywordsComp'] = []
data['keywordsSimp'] = []
chunker = nltk.RegexpParser(grammar) 
cont = 0
resultados = [text]
for registro in resultados:
	#cont=cont+1
	#if cont == 0: continue
	#if cont == 3: break
	sentences = tokenizarSentences(registro)
	for sentence in sentences:
		data['TotalSentences'] = len(sentences)
		extract = ExtraerData(sentence)
		listext = []
		for ex in extract:
			#print "safsdddddddddddddddddddddddddXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"ex
			for (label, frequency) in nltk.FreqDist(ex).items():
				estruDat = {"label":"", "frequency":"","dbpediaResource":"","DBpedRList":[], "type":0}
				#print "> ",label,"(",frequency,")"
				estruDat["type"] = extract.index(ex)
				estruDat["label"] = label
				estruDat["frequency"] = frequency
				estruDat["DBpedRList"] = extraerListRecursoDBpedia(label)
				listext.append(estruDat)
		#print sentence
		for l in Desambiguacion(listext, ExtraerNombres(sentence)):
			#print l['label'], ": ", l['type']
			if l['type'] == 0:
				data["entities"].append(l)
			if l['type'] == 1:
				data["keywordsComp"].append(l)
			if l['type'] == 2:
				data["keywordsSimp"].append(l)


print "\n ENTIDADES"
for d in data["entities"]:
	print "LABEL: ", d['label'] ,": ", d["dbpediaResource"]," (", len(d["DBpedRList"]),")"
	#print d["type"]
	#for l in d['DBpedRList']:	
	#	print l['uri']
	#	print l['uri'] , ": ", l['abstract'] 
	#	print ""
	print ""

print "\N KWYWORD COMPUESOTS"
for d in data["keywordsComp"]:
	print "LABEL: ", d['label'] ,": ", d["dbpediaResource"]," (", len(d["DBpedRList"]),")"
	#print d["type"]
	#for l in d['DBpedRList']:	
	#	print l['uri']
	#	print l['uri'] , ": ", l['abstract'] 
	#	print ""
	print ""

print "\N KEYWORD SIMPLES"
for d in data["keywordsSimp"]:
	print "LABEL: ", d['label'] ,": ", d["dbpediaResource"]," (", len(d["DBpedRList"]),")"
	#print d["type"]
	#for l in d['DBpedRList']:	
	#	print l['uri']
	#	print l['uri'] , ": ", l['abstract'] 
	#	print ""
	print ""
#print data["keywordsComp"]["list"]
print ""
#print data["keywordsSimp"]["list"]
print ""