
  $(function() {
    
    $('a#calculate').bind('click', function() {
        check1 = document.getElementById("check1");
        check2 = document.getElementById("check2");
        check3 = document.getElementById("check3");
        check4 = document.getElementById("check4");
        check5 = document.getElementById("check5");    
        
        function ColocarHtml(rst, rstUp){

            rst += "<p><a href=# id=verJson>Ver Json</a>";
            document.getElementById("resultado").innerHTML = rst;
            document.getElementById("resulUp").innerHTML = rstUp;
        }
        
        function Sentencias(data) {
            rst = "<h3>Sentencias</h3>"
                    rst += "<table>"
                    for (var i = 1; i <= data.result['TokensSentencias'].length; i++) 
                    {
                        rst += "<tr> <td>" + i +" </td><td>"+  data.result['TokensSentencias'][i-1] + "</td></tr>"
                    }
                    rst += "</table>"
            return rst;
        }

        function wordTokens(data) {
            rst = "<h3>Palabras</h3>"
                    rst += "<table>"
                    cont = 0
                    for (var i = 0; i < data.result['TokensPalabras'].length; i++) 
                    {
                        for (var j = 0; j < data.result['TokensPalabras'][i].length; j++) 
                        {    
                            cont = cont +1
                            rst += "<tr> <td>" + cont +" </td><td>"+  data.result['TokensPalabras'][i][j] + "</td></tr>"
                        }
                    }
                    rst += "</table>"
            return rst;              // the function returns the product of p1 and p2
        }

        function Etiquetado(data) {
            rst = "<h3>Etiquetas (PartofSpeech)</h3>"
                    rst += "<table>"
                    cont = 0
                    for (var i = 0; i < data.result['EtiquetadoPalabras'].length; i++) 
                    {
                        for (var j = 0; j < data.result['EtiquetadoPalabras'][i].length; j++) {
                            cont ++
                            rst += "<tr> <td>" + cont +" </td><td>"+  data.result['EtiquetadoPalabras'][i][j] + "</td></tr>"
                        }
                    }
                    rst += "</table>"
            return rst;              // the function returns the product of p1 and p2
        }

        function ExtracionEyK(data) {
            rst = "<h3>Extracionde Entidades y Keywords</h3>"
            rst += "<h4>Entidades</h4>"
            rst += "<table>"
            for (var i = 0; i < data.result['Entidades'].length; i++) 
            {
                rst += "<tr> <td>" + (i+1) +" </td><td>"+  data.result['Entidades'][i] + "</td></tr>"
            }
            rst += "</table>"

            rst += "<h4>Keywords Compuestas</h4>"
            rst += "<table>"
            for (var i = 0; i < data.result['KeywordsCompuestas'].length; i++) 
            {
                rst += "<tr> <td>" + (i+1) +" </td><td>"+  data.result['KeywordsCompuestas'][i] + "</td></tr>"
            }
            rst += "</table>"

            rst += "<h4>Keywords Simples</h4>"
            rst += "<table>"
            for (var i = 0; i < data.result['KeywordsSimples'].length; i++) 
            {
                rst += "<tr> <td>" + (i+1) +" </td><td>"+  data.result['KeywordsSimples'][i] + "</td></tr>"
            }
            rst += "</table>"
            return rst;              
        }

        function Enlace(data) {
            rst = "<h3>Enlace</h3>"
            rst += "<h4>Entidades</h4>"
            rst += "<table>"
            for (var i = 0; i < data.result['EntidadesDesambiguadas'].length; i++) 
            {
                rst += "<tr> <td>" + (i+1) +" </td><td>"+  data.result['EntidadesDesambiguadas'][i]['label'] ; 

                if (data.result['EntidadesDesambiguadas'][i]['dbpediaResource'])
                    rst += "</td><td>"+  "<a href=\""+data.result['EntidadesDesambiguadas'][i]['dbpediaResource'] +"\" >DBpedia</a> "+ "</td>";

                rst += "</tr>";
            }
            rst += "</table>"
            return rst;              
        }

        function Metadata(data, funcion) {
            var rstUp = "<div><table id = \"rstUp\">"
            //rstUp += "<tr class=\"metadataTitle\"> <td>Sentencias</td><td>Tokens</td><td>Entidades</td><td>Keywords Compuestas</td><td>Keywords Simples</td><td>Enlaces</td><tr>"
               if (funcion == 1)
                {
                    rstUp += "<tr class=\"metadataTitle\"> <td>Sentencias</td><tr>"
                    rstUp += "<tr class=\"metadataCont\"><td>"+data.result['NumSentencias']+"</td></tr>"
                } else if (funcion == 2)
                {
                    rstUp += "<tr class=\"metadataTitle\"> <td>Sentencias</td><td>Tokens</td><tr>"
                    rstUp += "<tr class=\"metadataCont\"><td>"+data.result['NumSentencias']+"</td><td>"+data.result['NumTokensPalabras']+"</td></tr>"
                    
                } else if (funcion == 3)
                {
                    rstUp += "<tr class=\"metadataTitle\"> <td>Sentencias</td><td>Tokens</td><tr>"
                    rstUp += "<tr class=\"metadataCont\"><td>"+data.result['NumSentencias']+"</td><td>"+data.result['NumTokensPalabras']+"</td></tr>"
                   
                } else if (funcion == 4)
                {
                    rstUp += "<tr class=\"metadataTitle\"> <td>Sentencias</td><td>Tokens</td><td>Entidades</td><td>Keywords Compuestas</td><td>Keywords Simples</td></tr>"
                    rstUp += "<tr class=\"metadataCont\"><td>"+data.result['NumSentencias']+"</td><td>"+data.result['NumTokensPalabras']+"</td><td>"+data.result['NumEntidades']+"</td><td>"+data.result['NumKeywordsCompuestas']+"</td><td>"+data.result['NumKeywordsSimples']+"</td></tr>"
                
                } else if (funcion == 5)
                {
                    rstUp += "<tr class=\"metadataTitle\"> <td>Sentencias</td><td>Tokens</td><td>Entidades</td><td>Keywords Compuestas</td><td>Keywords Simples</td><td>Enlazados</td></tr>"
                    rstUp += "<tr class=\"metadataCont\"><td>"+data.result['NumSentencias']+"</td><td>"+data.result['NumTokensPalabras']+"</td><td>"+data.result['NumEntidades']+"</td><td>"+data.result['NumKeywordsCompuestas']+"</td><td>"+data.result['NumKeywordsSimples']+"</td><td>"+data.result['NumEntidadesDesambiguadas']+"</td></tr>"
                    
                }
                rstUp += "</table>"
                return rstUp
        }

     

        function llamaServicio(servicio, funcion)
        {
            $.getJSON($SCRIPT_ROOT + servicio, {
            text: $('textarea#text').val()
            }, function(data) {
                var rst = "";
                var rstUp = ""
                if (funcion == 1)
                {
                    rst = Sentencias(data);
                } else if (funcion == 2)
                {
                    rst = wordTokens(data);
                    rst += Sentencias(data);
                } else if (funcion == 3)
                {
                    rst = Etiquetado(data);
                    rst += wordTokens(data);
                    rst += Sentencias(data);
                } else if (funcion == 4)
                {
                    rst = ExtracionEyK(data);
                    rst += Etiquetado(data);
                    rst += wordTokens(data);
                    rst += Sentencias(data);
                } else if (funcion == 5)
                {
                    rst = Enlace(data);
                    rst += ExtracionEyK(data);
                    rst += Etiquetado(data);
                    rst += wordTokens(data);
                    rst += Sentencias(data);
                }
                rstUp = Metadata(data, funcion)
                ColocarHtml(rst,rstUp);
                $('a#verJson').bind('click', function() {
            document.getElementById("json").innerHTML = JSON.stringify(data);
        });
            });
        }


         if(check5.checked)
        {
            llamaServicio('/v1/Desambiguacion',5)
        } else if(check4.checked)
        {
            llamaServicio('/v1/ExtracionEntidades',4)
        } else if (check3.checked) 
        {
            llamaServicio('/v1/Etiquetado',3)
        } else  if (check2.checked) 
        {
            llamaServicio('/v1/TokensPalabra',2)
        }  else if (check1.checked)
        {
            llamaServicio('/v1/TokensSentencias',1)
        }
        
      return false;
    });
  });

