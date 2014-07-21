#-*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
import requests
import urllib2
import json

class Procesar():	
	text1 = """Mercury is a major Roman god, being one of the Dii Consentes within the ancient Roman pantheon."""


	"""Mercury is a chemical element with the symbol Hg and atomic number 80."""
	"""It is commonly known as quicksilver and was 
	formerly named hydrargyrum (from Greek "hydr-" water and "argyros" silver).
	Mercury is the smallest and closest to the Sun of the eight planets in the Solar System,[a] with an orbital period of about 88 Earth days. 
	Mercury is a major Roman god, 
	being one of the Dii Consentes within the ancient Roman pantheon."""
	JsonResultado = ""
	#text = "Venus is the Roman goddess whose functions encompassed love, beauty, sex, fertility and prosperity. He is  a roman."
	def tokenizarSentences(self, text):
	    return nltk.sent_tokenize(text)

	def tokenizar(self, 	text):
	    return nltk.word_tokenize(text)

	def etiquetar(self, text_tokens):
	    return nltk.pos_tag(text_tokens)

	def chunkerWithTag(self, text_tag):
	    return nltk.ne_chunk(text_tag)

	def chunker(text_tag):
	    return nltk.ne_chunk(text_tag, binary=True)

	def extraerLabelRecurso(self, recurso): #return list[] labels de un recurso
		print "Extrayebdo Label de Recurso..."
		print "URI Recurso", recurso
		
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
		    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		    SELECT ?label
		    WHERE { <"""+recurso+"""> rdfs:label ?label }
		""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		nombres = []
		for result in results["results"]["bindings"]:
			nombres.append(result["label"]["value"])
		return nombres

	def extraerWikipediaLinkRecurso(self, recurso): #return list[] labels de un recurso
		#print "Extrayebdo Wikipedia Link de Recurso..."
		#print "URI Recurso", recurso
		
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
		    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
		    SELECT ?label
		    WHERE { <"""+recurso+"""> foaf:isPrimaryTopicOf ?label}
		""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		nombres = []
		for result in results["results"]["bindings"]:
			return result["label"]["value"]

	def extraerSubjetRecurso(self, recurso): #return list[] labels de un recurso
		#print "Extrayebdo Subject/Type Link de Recurso..."
		#print "URI Recurso", recurso
		
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
		    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX dcterms: <http://purl.org/dc/terms/>
			SELECT ?nombre
			WHERE
			{
			  <"""+recurso+"""> dcterms:subject ?nombre .
			} limit 3
		""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		#print results

		nombres = []
		for result in results["results"]["bindings"]:
			if len(result["nombre"]["value"]) > 3:
				print "type :",result["nombre"]["value"]
				nombres.append(result["nombre"]["value"])
		return nombres
		

	def extraerRecursosDbpedia(self, textEntities): #Resturn json resources from dbpedia
		print "Extrayendo Recurso desde Dbepdia..."
		url = "http://spotlight.dbpedia.org/rest/annotate/"
		headers = {'Accept': 'application/json'}
		datos = {
		    "text": textEntities,
		    "confidence": 0.3,
		    "support": 20,
		    "sparql" : ""
		    }
		r = requests.get(url, params=datos, headers=headers)
		#jsonResq = r.json()
		#print ">>JSON: ",jsonResq['Resources']
		#entidades = []
		#print jsonResq
		#print "JSON:", r.json()
		"""if r.json().has_key('Resources'):
						for ent in jsonResq['Resources']:
							if ent['@URI'] not in entidades:
								entidades.append(urllib2.unquote(ent['@URI']))
								print "	...", urllib2.unquote(ent['@URI'])  """
					#print "	TYPE Entity >> ", ent['@types']
		#print "( " , len(entidades) , ")"
		print r.json()
		return r.json()

	def extraerUriRecursosDbpedia(self, jsonResq): #return list[Uris]
		print "Extrayendo Uris de Recursos de Dbpedia..."
		entidades = []
		if jsonResq.has_key('Resources'):
			for ent in jsonResq['Resources']:
				uri = urllib2.unquote(ent['@URI'])
				#uri = ent['@URI']
				if uri not in entidades:
					entidades.append(uri)
					print "	...", uri
					#urllib2.unquote(ent['@URI'])
		return  entidades


	def extraerEntidades(self, text): #Return list[] entities dic{} >> list[{entidad:tag},{},{}]
		print "Extrayendo Entidades desde text..."
		treeChunk = self.chunkerWithTag(self.etiquetar(self.tokenizar(text)))
		entidades = []
		name = ""
		for x in treeChunk.subtrees():
			dicc = {}
			if x.node != 'S':
			    word = [w[0] for w in x.leaves()]
			    name = " ".join(word)
			    dicc['entidad'] = name 
			    dicc['tag'] = x.node
			    print "	... ", dicc['entidad'], " tag : ", dicc['tag'] 
			    entidades.append(dicc)
		return entidades

	def entInUri(self, ent, uris):
		for uri in uris:
			uri.replace('_', ' ')
			if (ent in uri) or (ent in uri.replace('_', ' ')):
				return uri
		return ""

	def entinLabel(self, ent, uris):
		for uri in uris:
			for lbl in self.extraerLabelRecurso(uri):
				if ent in lbl:
					return uri
		return ""

	def contruirEntidad(self, label, uri, tag):
		entidadDicc = {}
		entidadDicc['label'] = label
		#print "ERROR: ", uri
		entidadDicc['types'] = self.extraerSubjetRecurso(uri)
		if (bool(tag)): entidadDicc['types'].append(tag)
		entidadDicc['uri'] = {}
		entidadDicc['uri']['dbpedia'] = uri
		entidadDicc['uri']['wikipedia'] = self.extraerWikipediaLinkRecurso(uri)
		entidadDicc['uri']['freebase'] = uri
		return entidadDicc

	def unirEntidadesRecursos(self, entidadesNltk, urisRecursos):
		entidadesList = [] #list[] de diccionarios
		for ent in entidadesNltk:
			entidadDicc = {}
			uri = self.entInUri(ent['entidad'], urisRecursos)
			if not bool(uri) :
				uri = self.entinLabel(ent['entidad'], urisRecursos)
			entidadDicc = self.contruirEntidad(ent['entidad'] , uri, ent['tag'])

			if bool(entidadDicc):
				print "   !!!!",ent['entidad'] , " - ", uri
				entidadesList.append(entidadDicc)
				if bool(uri): urisRecursos.remove(uri)
		return entidadesList

	def recursoNoInEnti(self, listJsonEntidades, uri):
		for ent in listJsonEntidades:
			if uri == ent['uri']['dbpedia']:
				return False
		return True


	def getConceptos(self, listJsonEntidades, urisRecursos):
		#print jsonEntidades
		entidadesList = []
		entidadDicc = {}
		for urirec in urisRecursos:
			if bool(self.recursoNoInEnti(listJsonEntidades, urirec)):
				print " ??", urirec[len("http://dbpedia.org/resource/"):]
				lable = urirec[len("http://dbpedia.org/resource/"):]
				entidadDicc = self.contruirEntidad(lable.replace("_", " ") , urirec, "")
				entidadesList.append(entidadDicc)

		return entidadesList

	#print extraerLabelRecuro("<http://dbpedia.org/resource/Ecuador>")
	#entidades = extraerEntidades(text)

	def ProcesarTextoNltkDBpedia(self, text):
		print ""
		text = text.replace('"' , '')
		text = text.replace('\n' , ' ')
		text = text.replace('\t' , ' ')
		JsonResultado = {}
		JsonResultado['@text'] = text
		JsonResultado['@entidades'] = []
		JsonResultado['@conceptos'] = []
		sentencias = self.tokenizarSentences(text)
		for sente in sentencias:
			print ""
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> SENTENCIA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n *** " + sente
			entidadesNltk   = self.extraerEntidades(sente) # list[diccionario{}] (text)
			jsonRecurosos = self.extraerRecursosDbpedia(sente) #json  (text)
			urisRecursos = self.extraerUriRecursosDbpedia(jsonRecurosos) #list[] de uris de recuros de dbpedia    (json) 
			entidades = self.unirEntidadesRecursos(entidadesNltk, urisRecursos)
			for e in entidades:
				JsonResultado['@entidades'].append(e)
			conceptos = self.getConceptos(JsonResultado['@entidades'], urisRecursos)
			for c in conceptos:
				JsonResultado['@conceptos'].append(c)
			
			#JsonResultado['@entidaes'] = entidadesList
		print  json.loads(json.dumps(JsonResultado))
		return json.loads(json.dumps(JsonResultado))

	def ProcesarTextoNltk(self, text):
		print ""
		text = text.replace('"' , '')
		text = text.replace('\n' , ' ')
		text = text.replace('\t' , ' ')
		JsonResultado = {}
		JsonResultado['@text'] = text
		JsonResultado['@entidades'] = []
		#JsonResultado['@conceptos'] = []
		sentencias = self.tokenizarSentences(text)
		for sente in sentencias:
			print ""
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> SENTENCIA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n *** " + sente
			entidadesNltk   = self.extraerEntidades(sente) # list[diccionario{}] (text)
			for et in entidadesNltk:
				JsonResultado['@entidades'].append(et)
		print  json.loads(json.dumps(JsonResultado))
		return json.loads(json.dumps(JsonResultado))