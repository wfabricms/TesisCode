from ProcesarTexto import ProcesarTexto
from DBpediaInteraccion import DbepdiaInteraccionRecursos
from Desambiguacion import Desambiguacion

class ConstruccionServicios():
	#objProcesarTexto = ProcesarTexto()
	def TokenizacionSentencias(self, text):
		data = {}
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		listSentencias = objProcesarTexto.tokenizarSentencias(text)
		data['NumSentencias'] =  len(listSentencias)
		data['TokensSentencias'] = listSentencias
		#print data
		return data

	def EtiquetarTT(self, text):
		data = self.TokenizacionSentencias(text)
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
				print token[0]
				print palabras
			EtiquetasPalabras.append(restTokensPalabras)
			TokensEnPalabras.append(palabras)
		data['EtiquetadoPalabras']  = EtiquetasPalabras 
		data['TokensPalabras']  = TokensEnPalabras 
		return data

	def TokenizarTT(self, text):
		data = self.TokenizacionSentencias(text)
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
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		data['KeywordsSimples'] = []
		data['KeywordsCompuestas'] = []
		data['Entidades'] = []
		listaEntidades = []
		data['EntidadesDesambiguadas'] = []
		for sentenciaTokenizada in data['EtiquetadoPalabras']:
			entidades = []
			data['KeywordsSimples'] = data['KeywordsSimples'] + [w for (w, x) in sentenciaTokenizada if len(w)>1  and x =='NN' or x =='NNS']
			treeChunk = objProcesarTexto.AplicarChunker(sentenciaTokenizada)
			for x in treeChunk.subtrees():
				if x.node == 'SUST':	
					word = [w[0] for w in x.leaves()]
					name = " ".join(word)
					if len(name) >1 and name not in data['KeywordsSimples']: data['KeywordsCompuestas'].append(name)
				if x.node == 'ENTCOMP' or x.node == 'ENT':
					word = [w[0] for w in x.leaves()]
					name = " ".join(word)
					if len(name) >1: entidades.append(name)
			data['Entidades'] = data['Entidades']  + entidades
			data['NumKeywordsSimples'] = len(data['KeywordsSimples'])
			data['NumKeywordsCompuestas'] = len(data['KeywordsCompuestas'])
			data['NumEntidades'] = len(data['Entidades'])
			if d == 1:
				objDbInteracion = DbepdiaInteraccionRecursos()
				objDesamb = Desambiguacion()
				#for entidad in entidades+data['KeywordsSimples']+data['KeywordsCompuestas']:
				#for entidad in entidades:
				for entidad in entidades + data['KeywordsCompuestas']:
					estruDat = {"label":"", "frequency":"","dbpediaResource":"","DBpedRList":[], "type":0}
					estruDat["label"] = entidad
					estruDat['DBpedRList'] = objDbInteracion.extraerListRecursoDBpedia(entidad)
					listaEntidades.append(estruDat)
				if data['EtiquetadoPalabras'].index(sentenciaTokenizada) == len (data['EtiquetadoPalabras']) -1: 
					data['EntidadesDesambiguadas'] = objDesamb.LeskAlgoritm(listaEntidades, objDbInteracion.ExtraerNombres(data['TokensSentencias'][data['EtiquetadoPalabras'].index(sentenciaTokenizada)]))
				data['NumEntidadesDesambiguadas'] = len(data['EntidadesDesambiguadas'])
		return data