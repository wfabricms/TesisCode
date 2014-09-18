Mercury is a major Roman god, being one of the Dii Consentes within the ancient Roman pantheon.Mercury is a chemical element with the symbol Hg and atomic number 80. It is commonly known as quicksilver and was 	formerly named hydrargyrum (from Greek "hydr-" water and "argyros" silver). Mercury is the smallest and closest to the Sun of the eight planets in the Solar System,[a] with an orbital period of about 88 Earth days. Mercury is a major Roman god, being one of the Dii Consentes within the ancient Roman pantheon.

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT distinct ?recurso ?amb

WHERE {
?recurso ?predicado ?text.
OPTIONAL { ?recurso dbpedia-owl:wikiPageDisambiguates ?amb }
FILTER regex(?recurso, "http://dbpedia.org/")
FILTER (?predicado = foaf:name || ?predicado = rdfs:label)
FILTER regex(?text, '^ecuador$', 'i' )
}


PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?recurso ?amb
WHERE {
		?recurso ?predicado 'Loja'@en.
		OPTIONAL { ?recurso dbpedia-owl:wikiPageDisambiguates ?amb }
		FILTER regex(?recurso, "http://dbpedia.org/", "i")
		FILTER (?predicado = rdfs:label || ?predicado = foaf:name)
}

select ?o where {<http://dbpedia.org/resource/Autism> <http://www.w3.org/2000/01/rdf-schema#comment> ?o} LIMIT 100


encoded_url = quote_plus(recurso, safe='/:')
	tittletyope = quote_plus(tittletyope, safe='/:')
	SparqlQuery = """
	    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
		PREFIX foaf: <http://xmlns.com/foaf/0.1/>

		SELECT distinct ?x ?amb
		WHERE {
			?x ?predicado ?text.
			OPTIONAL { ?x dbpedia-owl:wikiPageDisambiguates ?amb }
			FILTER (?predicado = foaf:name || ?predicado = rdfs:label)
			FILTER (?text = '%s'@en || ?text = '%s'@en || ?text = '%s'@en || ?text = '%s'@en)
		}
	""" %(encoded_url.lower(), encoded_url.upper(), tittletyope, encoded_url)



PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT *
WHERE { ?label rdfs:label ?term .
FILTER (lcase(str(?term)) = "loja") .
}


<http://dbpedia.org/resource/2010-11_Scottish_Youth_Cup> <http://dbpedia.org/ontology/wikiPageRedirects> <http://dbpedia.org/resource/2010%E2%80%9311_Scottish_Youth_Cup> .



PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT distinct *
WHERE {
	?x ?predicado ?text.
	OPTIONAL { ?x dbpedia-owl:wikiPageDisambiguates ?amb }
	OPTIONAL { ?x dbpedia-owl:wikiPageRedirects ?xredir }
	OPTIONAL { ?xredir dbpedia-owl:wikiPageDisambiguates ?amb1 }
	FILTER (?predicado = foaf:name || ?predicado = rdfs:label)
	FILTER (?text = 'Ez'@en)
}