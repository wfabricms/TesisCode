from ProcesarTexto import ProcesarTexto
import json
import urllib2
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import nltk
from nltk.corpus import stopwords
import unicodedata
objProcesarTexto = ProcesarTexto()
class DbepdiaInteraccionRecursos():

	
	def PreparaFiltroTexto(self, recurso):
		tittletype = ""	
		for s in recurso.split():
			if s.lower() in stopwords.words('english') or s.lower() in stopwords.words('spanish'):
				tittletype = tittletype + s.lower() + ' ' 
			else:
				tittletype = tittletype + s.title() + ' ' 
		tittletype = tittletype[:-1]
		return tittletype

	def getQuery(self, term):
		SparqlQueryPrefix = """
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
			PREFIX foaf: <http://xmlns.com/foaf/0.1/>
			"""
		SparqlQuery = SparqlQueryPrefix+"""
			SELECT distinct ?x ?amb ?redir ?amb1
			From <http://data.utpl.edu.ec/dbpedia> 
			WHERE {
				?x ?predicado '"""+term+"""'@en.
				OPTIONAL { ?x dbpedia-owl:wikiPageDisambiguates ?amb }
				OPTIONAL { ?x dbpedia-owl:wikiPageRedirects ?redir }
				OPTIONAL { ?redir dbpedia-owl:wikiPageDisambiguates ?amb1 }
			}
		""" #%(tittletyope, recurso) #%(encoded_url.lower(), encoded_url.upper(), tittletyope, encoded_url)

		"""
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
			PREFIX foaf: <http://xmlns.com/foaf/0.1/>	

		SELECT distinct ?x ?amb ?redir ?amb1 ?amb2 ?redir2 ?amb3
			WHERE {
				?x ?predicado ?text.
				OPTIONAL { ?x dbpedia-owl:wikiPageDisambiguates ?amb }
				OPTIONAL { ?amb2 dbpedia-owl:wikiPageDisambiguates ?x }
				OPTIONAL { ?amb2 dbpedia-owl:wikiPageRedirects ?redir2 }
				OPTIONAL { ?amb2 dbpedia-owl:wikiPageDisambiguates ?amb3 }
				OPTIONAL { ?x dbpedia-owl:wikiPageRedirects ?redir }
				OPTIONAL { ?redir dbpedia-owl:wikiPageDisambiguates ?amb1 }
				FILTER (?predicado = foaf:name || ?predicado = rdfs:label)
				FILTER (?text = 'PE'@en)
			}
		"""

		return SparqlQuery

	def extraeListaDesdeJson(self, results):
		uris = []
		for result in results["results"]["bindings"]:
			if "amb1" in result.keys():
				if result["amb1"]["value"]  not in uris and "http://dbpedia.org/resource/" in result["amb1"]["value"] and "Category:" not in result["amb1"]["value"]: uris.append(result["amb1"]["value"])	
			elif "redir" in result.keys():
				if result["redir"]["value"] not in uris and "http://dbpedia.org/resource/" in result["redir"]["value"]  and "Category:" not in result["redir"]["value"]: uris.append(result["redir"]["value"])	
			elif "amb" in result.keys():
				if result["amb"]["value"]   not in uris and "http://dbpedia.org/resource/" in result["amb"]["value"]  and "Category:" not in result["amb"]["value"]: uris.append(result["amb"]["value"])	
			else:
				if result["x"]["value"]     not in uris and "http://dbpedia.org/resource/" in result["x"]["value"]  and "Category:" not in result["x"]["value"]: uris.append(result["x"]["value"])		
		return uris

	def ejecutarQuery(self, SparqlQuery, servidor):
		sparql = SPARQLWrapper(servidor)
		sparql.setQuery(SparqlQuery)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		return results	

	def extraerListRecursoDBpedia(self, recurso): #return list[] labels de un recurso
		#print "URI Recurso: ", recurso
		#print SparqlQuery
		#servidor = "http://localhost:8890/sparql"
		servidor = "http://apolo.utpl.edu.ec/vtitanio/sparql"
		
		filterText = self.PreparaFiltroTexto(recurso)
		#print (filterText)
		#print (recurso)
		if recurso == filterText:
			results = self.ejecutarQuery(self.getQuery(recurso),servidor)
		else:
			results = self.ejecutarQuery(self.getQuery(filterText),servidor)
			if len(results["results"]["bindings"]) == 0 :
				results = self.ejecutarQuery(self.getQuery(recurso),servidor)
			#results = self.ejecutarQuery(SparqlQuery,servidor)


		if not len(results["results"]["bindings"]) == 0 :
			uris = self.extraeListaDesdeJson(results)
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
				abstract = self.ExtraerNombres(objProcesarTexto.tokenizarSentencias(results["results"]["bindings"][0]["abstract"]["value"])[0])
				recDbpediaAbstr["abstract"] = abstract
			else:
				recDbpediaAbstr["abstract"] = recDbpediaAbstr["uri"][len("http://dbpedia.org/resource/"):].replace('_',' ').replace('(','').replace(')','').split()
			recursosDbpediaAbstr.append(recDbpediaAbstr)
		return recursosDbpediaAbstr # return [{"uri":"", "abstract":""}, {"uri":"", "abstract":""}]

	def ExtraerNombres(self, sentence):
	 	ett = objProcesarTexto.etiquetar(objProcesarTexto.tokenizarPalabras(sentence))
	 	abstract = []
		for (w, x) in ett:
			if len(w)>2 and x =='NNP' or x =='NNPS' or x =='NN' or x =='NNS'or x =='JJ':
				#if len(w)>2  and x =='NNP' and w not in abstract:
				#if w not in abstract: 
				abstract.append(w.capitalize())
		return abstract

	def dataTypeExtract(self, results):
		uris = []
		for result in results["results"]["bindings"]:
			if "types" in result.keys():
				uris.append(result["types"]["value"])
		return uris

	def getQueryType(elf, term):
		querytype = """select distinct * where {<"""+term+"""> rdf:type ?types.}"""
		return querytype

	def TypeExtract(self, recursos):
		a = [1,2,3]
		servidor = "http://apolo.utpl.edu.ec/vtitanio/sparql"
		for recurso in recursos:
			if recurso['dbpediaResource'] != "" :
				print "TYPE DATA >> ", recurso['dbpediaResource']
				results = self.ejecutarQuery(self.getQueryType(recurso['dbpediaResource']),servidor)
				recurso['dbpediaResourceType'] = self.dataTypeExtract(results)
		return recursos