class Desambiguacion():

	def CalcularConcordancia(self, abstract_j, abstract_l, listSentence):
		concordancia = 0
		for word_j in abstract_j:
			for word_l in abstract_l + listSentence:
				if word_l.lower() == word_j.lower(): concordancia = concordancia + 1
		return concordancia
		
	def LeskAlgoritm(self, listData, listSentence):
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
							SCORE = SCORE + self.CalcularConcordancia(sense_j['abstract'], sense_l['abstract'], listSentence)
				if SCORE > BEST_SCORE:
					BEST_SCORE = SCORE
					BEST_SENSE = sense_j['uri']

			if BEST_SCORE > 0:
				word_i['dbpediaResource'] = BEST_SENSE
				print "SCORE", BEST_SCORE, ", ", BEST_SENSE
			else:
				print word_i,": ambiguo"
		return listData