from ProcesarTexto import ProcesarTexto

class ConstruccionServicios():
	#objProcesarTexto = ProcesarTexto()
	def TokenizacionSentencias(self, text):
		data = {}
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		listSentencias = objProcesarTexto.tokenizarSentencias(text)
		data['NumSentencias'] =  len(listSentencias)
		data['TokensSentencias'] = listSentencias
		print data
		return data

	def EtiquetarTT(self, text):
		data = self.TokenizacionSentencias(text)
		TokensEnPalabras = []
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		data['NumTokensPalabras'] = 0
		for sentencia in data['TokensSentencias']:
			restTokensPalabras = objProcesarTexto.EtiquetarTreeTagger(sentencia)
			data['NumTokensPalabras'] = data['NumTokensPalabras'] + len(restTokensPalabras)
			TokensEnPalabras.append(restTokensPalabras)
		data['EtiquetadoPalabras']  = TokensEnPalabras 
		return data


	def ExtracionEntidadesAndKeywords(self, text, d):
		data = self.EtiquetarTT(text)
		#global objProcesarTexto
		objProcesarTexto = ProcesarTexto()
		data['KeywordsSimples'] = []
		data['KeywordsCompuestas'] = []
		data['Entidades'] = []
		
		for sentenciaTokenizada in data['EtiquetadoPalabras']:
			entidades = []
			data['KeywordsSimples'].append([w for (w, x) in sentenciaTokenizada if len(w)>1  and x =='NN' or x =='NNS'])
			treeChunk = objProcesarTexto.AplicarChunker(sentenciaTokenizada)
			for x in treeChunk.subtrees():
				#print x
				if x.node == 'SUST':	
					word = [w[0] for w in x.leaves()]
					name = " ".join(word)
					if len(name) >1 and name not in data['KeywordsSimples']: data['KeywordsCompuestas'].append(name)
				if x.node == 'ENTCOMP' or x.node == 'ENT':
					word = [w[0] for w in x.leaves()]
					name = " ".join(word)
					if len(name) >1: entidades.append(name)
			
			if d == 1:
				
			print data['EtiquetadoPalabras'].index(sentenciaTokenizada)	, " - ", data['TokensSentencias'].index(data['TokensSentencias'][data['EtiquetadoPalabras'].index(sentenciaTokenizada)])		
		return data
		

	
	






