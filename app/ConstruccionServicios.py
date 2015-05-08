from ProcesarTexto import ProcesarTexto
from DBpediaInteraccion import DbepdiaInteraccionRecursos
from Desambiguacion import Desambiguacion

class ConstruccionServicios():
	#objProcesarTexto = ProcesarTexto()
	def TokenizacionSentencias(self, text):
		print "TOKENIZACION DE SENTECIAS"
		if len(text)  < 2:
			return {"err":"error no text"}
		objProcesarTexto = ProcesarTexto()
		text = objProcesarTexto.validateTextCharacter(text)
		lang =  objProcesarTexto.validateTextLenguage(text)
		if lang != 'english':
			#return {"err":"Text is not English. "+lang+" unsupported"}
			return {"err":"Text unsupported or language unsupported"}
		data = {}
		listSentencias = objProcesarTexto.tokenizarSentencias(text)
		data['NumSentencias'] =  len(listSentencias)
		data['TokensSentencias'] = listSentencias
		#print data
		#print data['TokensSentencias'][0]
		#if objProcesarTexto.validateTextLenguage("hola mundo") != "english" :
		#	print "NO es ingles"
		#	return {"err":"Language not supported "}
		
		return data

	def EtiquetarTT(self, text):
		data = self.TokenizacionSentencias(text)
		print "ETIQUETADO"
		if "err" in data:
			#print "err etiquetqad"
			return data
		EtiquetasPalabras = []
		TokensEnPalabras = []
		palabras = []
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		data['NumTokensPalabras'] = 0
		for sentencia in data['TokensSentencias']:
			restTokensPalabras = objProcesarTexto.EtiquetarTreeTagger(sentencia)
			data['NumTokensPalabras'] = data['NumTokensPalabras'] + len(restTokensPalabras)
			palabras = []
			for token in restTokensPalabras:
				palabras.append(token[0])
				#print token[0]
				#print palabras
			EtiquetasPalabras.append(restTokensPalabras)
			TokensEnPalabras.append(palabras)
		data['EtiquetadoPalabras']  = EtiquetasPalabras 
		data['TokensPalabras']  = TokensEnPalabras 
		return data

	def TokenizarTT(self, text):
		data = self.TokenizacionSentencias(text)
		print "TOKENIZACION DE PALABRAS"
		if "err" in data:
			return data
		TokensEnPalabras = []
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		data['NumTokensPalabras'] = 0
		for sentencia in data['TokensSentencias']:
			restTokensPalabras = objProcesarTexto.tokenizarTreeTagger(sentencia)
			data['NumTokensPalabras'] = data['NumTokensPalabras'] + len(restTokensPalabras)
			TokensEnPalabras.append(restTokensPalabras)

		data['TokensPalabras']  = TokensEnPalabras 
		return data

	#tokenizarTreeTagger

	def ExtracionEntidadesAndKeywords(self, text, d):
		data = self.EtiquetarTT(text)
		print "EXTRACCION DE ENTIDADES"
		if "err" in data:
			return data
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		data['KeywordsSimples'] = []
		data['KeywordsCompuestas'] = []
		data['Entidades'] = []
		listaEntidades = []
		data['EntidadesDesambiguadas'] = []
		data['KeyWordsCompDesambiguadas'] = []
		data['KeyWordsSimpDesambiguadas'] = []
		for sentenciaTokenizada in data['EtiquetadoPalabras']:
			entidades = []
			listaEntidades = []
			KeywordsCompuestas = []
			KeywordsSimples = []
			KeywordsSimples = KeywordsSimples + [w for (w, x) in sentenciaTokenizada if len(w)>1  and x =='NN' or x =='NNS']
			treeChunk = objProcesarTexto.AplicarChunker(sentenciaTokenizada)
			for x in treeChunk.subtrees():
				#print "NODE > ", x.node
				#if x.label == 'SUST':
				if x.node == 'SUST':
					word = [w[0] for w in x.leaves()]
					name = " ".join(word)
					if len(name) >1 and name not in KeywordsSimples: KeywordsCompuestas.append(name)
				if x.node == 'ENTCOMP' or x.node == 'ENT':
					word = [w[0] for w in x.leaves()]
					name = " ".join(word)
					if len(name) >1: entidades.append(name)
			data['Entidades'] = data['Entidades']  + entidades
			data['KeywordsCompuestas'] = data['KeywordsCompuestas']  + KeywordsCompuestas
			data['KeywordsSimples'] = data['KeywordsSimples']  + KeywordsSimples
			data['NumKeywordsSimples'] = len(data['KeywordsSimples'])
			data['NumKeywordsCompuestas'] = len(data['KeywordsCompuestas'])
			data['NumEntidades'] = len(data['Entidades'])
			if d == 1:
				objDbInteracion = DbepdiaInteraccionRecursos()
				#print "ENTIDADES"
				typeresource = 'EntidadesDesambiguadas'
				data = self.RecolectDataEntitiesKComp(data,entidades, sentenciaTokenizada, objDbInteracion, typeresource)
				#print "KEYWORDS COMPUESTAS"
				typeresource = 'KeyWordsCompDesambiguadas'
				data = self.RecolectDataEntitiesKComp(data,KeywordsCompuestas, sentenciaTokenizada, objDbInteracion, typeresource)
				
				#print "KEYWORDS SIMPLES"
				KeywordsSimples = list(set(KeywordsSimples))
				for entidad in KeywordsSimples:
					#print "  >>  ", entidad
					estruDat = {"label":"", "dbpediaResource":"","dbpediaResourceType":[],"DBpedRList":[]}
					estruDat["label"] = entidad
					for i in data['KeyWordsSimpDesambiguadas']:
						if entidad in i['label']:
							estruDat['dbpediaResource'] = i['dbpediaResource']
							break
					if estruDat['dbpediaResource'] == "":
						estruDat['dbpediaResource'] = objDbInteracion.extraerRecursosKeywordsSimples(entidad)
					listaEntidades.append(estruDat)
					data['KeyWordsSimpDesambiguadas'].append(estruDat)
				
				
		#print "CONTANDO Y ELIMINADO"
		#print ""
		#print "ENTIDADES"
		typeresource = 'EntidadesDesambiguadas'
		data = self.contarDataEnlazada(data, typeresource)
		#print "KEYWORDS COMPUESTAS"
		typeresource = 'KeyWordsCompDesambiguadas'
		data = self.contarDataEnlazada(data, typeresource)
		#print "KEYWORDS SIMPLES"
		typeresource = 'KeyWordsSimpDesambiguadas'
		data = self.contarDataEnlazada(data, typeresource)
		data['NumEntidadesDesambiguadas'] = len(data['EntidadesDesambiguadas']) + len(data['KeyWordsCompDesambiguadas']) + len(data['KeyWordsSimpDesambiguadas'])
		#print "TYPO DE RECURSOS"
		if data['EtiquetadoPalabras'].index(sentenciaTokenizada) == len (data['EtiquetadoPalabras']) -1: 
			for i in data['EntidadesDesambiguadas']:
				data['EntidadesDesambiguadas'] = objDbInteracion.TypeExtract(data['EntidadesDesambiguadas'])
			for i in data['KeyWordsCompDesambiguadas']:
				data['KeyWordsCompDesambiguadas'] = objDbInteracion.TypeExtract(data['KeyWordsCompDesambiguadas'])
			for i in data['KeyWordsSimpDesambiguadas']:
				data['KeyWordsSimpDesambiguadas'] = objDbInteracion.TypeExtract(data['KeyWordsSimpDesambiguadas'])
				
		return data

	def contarDataEnlazada(self, data, typeresource):
		m = []
		for d in data[typeresource]:
			if d['dbpediaResource'] == "": 
				continue	
			for e in data[typeresource]:
				if e['dbpediaResource'] == "": 
					continue
				#print "    >>    	", d['label'], " ", data[typeresource].index(d)
				if d['dbpediaResource'] != e['dbpediaResource'] and d not in m:
					#print "    >>    	XXXXXx", d['label'], " ", data[typeresource].index(d)
					m.append(d)
		data[typeresource] = m
		return data

	def RecolectDataEntitiesKComp (self, data, entidades, sentenciaTokenizada, objDbInteracion, typeresource):
		objDesamb = Desambiguacion()
		listaEntidades = []
		entidades = list(set(entidades))
		for entidad in entidades:
			#print "ENTIDAD = ", entidad
			find = False
			#print "  >>  ", entidad
			estruDat = {"label":"", "dbpediaResource":"","dbpediaResourceType":[],"DBpedRList":[]}
			estruDat["label"] = entidad
			

			#print "  >> ** ", entidad
			if estruDat['DBpedRList'] == []:
				estruDat['DBpedRList'] = objDbInteracion.extraerListRecursoDBpedia(entidad)
			#print estruDat['label']
			#print estruDat['DBpedRList']
			listaEntidades.append(estruDat)
		data[typeresource] += objDesamb.LeskAlgoritm(listaEntidades, objDbInteracion.ExtraerNombres(data['TokensSentencias'][data['EtiquetadoPalabras'].index(sentenciaTokenizada)]))
		return data
		

