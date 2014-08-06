from Etiquetado import ProcesarTextov1
import ListaRecursos

#lista = [[URI, Label, Context]
#http://www.w3.org/2002/07/owl#sameAs
newfile = "NoraBOOKS2"
sameAs = "http://www.w3.org/2002/07/owl#sameAs"


objP = ProcesarTextov1()


lista = ListaRecursos.Lista
lista2 = []
for l in lista:
	estruDat = {"label":"", "frequency":"","dbpediaResource":"","DBpedRList":[], "URI":""}
	estruDat["label"] = l[1]
	estruDat["URI"] = l[0]
	estruDat["DBpedRList"] = objP.extraerListRecursoDBpedia(l[1])
	lista2.append(estruDat)
lista2 = objP.Desambiguacion(lista2, objP.ExtraerNombres(l[2]))

cont = 0
file = open("/home/fabricio/Escritorio/DataResult/"+newfile+".nt", "w")
#file.write("hello world in the new file\n")
for l in lista2:
	if l['dbpediaResource'] !=  "":
		triple = "<"+l["URI"]+">"+" "+"<"+sameAs+">"+" "+"<"+l["dbpediaResource"]+"> ."
		print triple
		file.write(triple)
		file.write("\n")
		cont = cont +1;
#file.write("#FIN\n")
file.close()
print cont, "/", len(lista)		
#print lista2

