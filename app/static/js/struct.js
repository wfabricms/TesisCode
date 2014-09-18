
  $(function() {
    
    $('a#calculate').bind('click', function() {
        check1 = document.getElementById("check1");
        check2 = document.getElementById("check2");
        check3 = document.getElementById("check3");
        check4 = document.getElementById("check4");
        check5 = document.getElementById("check5");    
        
        function ColocarHtml(rst, rstUp){

            //rst += "<p><a href=# id=verJson>Ver Json</a>";
            document.getElementById("resultado").innerHTML = rst;
            document.getElementById("resulUp").innerHTML = rstUp;
        }

        function Sentencias(data) {
            rst = "<div id=\"opcion1\" style=\"position: absolute;\" class=\"center\">"
            //rst += "<h3>Sentencias</h3>"
                    rst += "<table>"
                    rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Sentencias </td></tr>"
                    for (var i = 1; i <= data.result['TokensSentencias'].length; i++) 
                    {
                        rst += "<tr class=\"bodyRest\"> <td class=\"colNum1\">" + i +"</td><td class=\"colData1\">"+  data.result['TokensSentencias'][i-1] + "</td></tr>"    
                    }
            rst += "</table>"
            rst += "</div>"
            return rst;
        }

        function wordTokens(data) {
            rst = "<div id=\"opcion2\" style=\"position: absolute; display: none;\">"
            
                    cont = 0
                    for (var i = 0; i < data.result['TokensPalabras'].length; i++) 
                    {
                        rst += "<p class=\"subtRest\">Sentencia #"+(i+1)+"</p>"
                        rst += "<table>"
                        rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Token </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Token </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Token </td></tr>"
                        for (var j = 0; j < data.result['TokensPalabras'][i].length; ) 
                        { 
                        rst += "<tr>"
                            t = 0

                            while (j < data.result['TokensPalabras'][i].length &&  t != 3 )
                            {
                                t ++;
                                cont ++;
                                rst += "<td class=\"colNum1\">" + cont +" </td><td class=\"colData1\">"+  data.result['TokensPalabras'][i][j] + "</td>";
                                j ++;
                                if(j < data.result['TokensPalabras'][i].length)
                                {
                                    rst += "<td></td>"
                                }
                            }
                            rst += "</tr>"

                        }
                        rst += "</table>" 
                    }
                    
            rst += "</div>"
            return rst;              // the function returns the product of p1 and p2
        }

        function Etiquetado(data) {
            rst = "<div id=\"opcion3\" style=\"position: absolute; display: none;\">"
            
                    cont = 0
                    for (var i = 0; i < data.result['EtiquetadoPalabras'].length; i++) 
                    {
                        rst += "<p class=\"subtRest\">Sentencia #"+(i+1)+"</p>"
                        rst += "<table>"
                         rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Token </td><td class=\"colData2\"> Etiqueta </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Token </td><td class=\"colData2\"> Etiqueta </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Token </td><td class=\"colData2\"> Etiqueta </td></tr>"
                        for (var j = 0; j < data.result['EtiquetadoPalabras'][i].length;) 
                        { 
                        rst += "<tr>"
                            t = 0

                            while (j < data.result['EtiquetadoPalabras'][i].length &&  t != 3 )
                            {
                                t ++;
                                cont ++;  
                                rst += "<td class=\"colNum1\">" + cont +" </td><td class=\"colData1\">"+  data.result['EtiquetadoPalabras'][i][j][0] + "</td><td class=\"colData1\">"+  data.result['EtiquetadoPalabras'][i][j][1]+ "</td>";
                                j ++;
                                if(j < data.result['EtiquetadoPalabras'][i].length)
                                {
                                    rst += "<td></td>"
                                }
                            }
                            rst += "</tr>"
                        }
                        rst += "</table>"
                    }
            rst += "</div>"
            return rst;              // the function returns the product of p1 and p2
        }

        function ExtracionEyK(data) {
            rst = "<div id=\"opcion4\" style=\"position: absolute; display: none;\">"
            rst += "<p class=\"subtRest\">Entidades</p>"
            rst += "<table>"
            rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Entidades </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Entidades </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Entidades </td></tr>"
            
            for (var i = 0; i < data.result['Entidades'].length;) 
            {
                rst += "<tr>"
                t=0;
                while (i < data.result['Entidades'].length &&  t != 3 )
                {
                    t ++;
                    rst += "<td class=\"colNum1\">" + (i+1) +" </td><td class=\"colData1\">"+  data.result['Entidades'][i] + "</td>"
                    i ++;
                    if(i < data.result['Entidades'].length)
                    {
                        rst += "<td></td>"
                    }
                }
                rst += "</tr>"
            }
            rst += "</table>"

            rst += "<p class=\"subtRest\">Keywords Compuestas</p>"
            rst += "<table>"
            rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Keywords Compuestas </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Keywords Compuestas </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Keywords Compuestas </td></tr>"
            for (var i = 0; i < data.result['KeywordsCompuestas'].length; ) 
            {

                rst += "<tr>"
                t=0;
                while (i < data.result['KeywordsCompuestas'].length &&  t != 3 )
                {
                    t ++;
                    rst += "<td class=\"colNum1\">" + (i+1) +" </td><td class=\"colData1\">"+  data.result['KeywordsCompuestas'][i] + "</td>"
                    i ++;
                    if(i < data.result['KeywordsCompuestas'].length)
                    {
                        rst += "<td></td>"
                    }
                }
                rst += "</tr>"
                
            }
            rst += "</table>"


            rst += "<p class=\"subtRest\">Keywords Simples</p>"
            rst += "<table>"
            rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Keywords Simples </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Keywords Simples </td><td></td><td class=\"colNum2\"> # </td><td class=\"colData2\"> Keywords Simples </td></tr>"
            for (var i = 0; i < data.result['KeywordsSimples'].length; ) 
            {

                rst += "<tr>"
                t=0;
                while (i < data.result['KeywordsSimples'].length &&  t != 3 )
                {
                    t ++;
                    rst += "<td class=\"colNum1\">" + (i+1) +" </td><td class=\"colData1\">"+  data.result['KeywordsSimples'][i] + "</td>"
                    i ++;
                    if(i < data.result['KeywordsSimples'].length)
                    {
                        rst += "<td></td>"
                    }
                }
                rst += "</tr>"
                
            }
            rst += "</table>"
            rst += "</div>"
            return rst;              
        }

        function Enlace(data) {
            rst = "<div id=\"opcion5\" style=\"position: absolute; display: none;\">"
            rst += "<p class=\"subtRest\">Entidades</p>"
            rst += "<table>"
            rst += "<tr> <td class=\"colNum2\"> # </td><td class=\"colData2\"> Entidad </td><td class=\"colData2\"> Tipo </td><td class=\"colData2\"> Enlace </td></tr>"
            for (var i = 0; i < data.result['EntidadesDesambiguadas'].length; i++) 
            {
                rst += "<tr> <td class=\"colNum1\">" + (i+1) +" </td><td class=\"colData1\">"+  data.result['EntidadesDesambiguadas'][i]['label'] +"</td>" ; 

                if (data.result['EntidadesDesambiguadas'][i]['dbpediaResource'])
                {
                    rst += "<td  class=\"colData1\">"
                    for ( var j = 0; j <  data.result['EntidadesDesambiguadas'][i]['dbpediaResourceType'].length; j++)
                    {
                        rst += "<a href = \""+data.result['EntidadesDesambiguadas'][i]['dbpediaResourceType'][j] + "\">"+ data.result['EntidadesDesambiguadas'][i]['dbpediaResourceType'][j] +"</a><br>"
                    }
                    rst += "</td>"
                    rst += "<td class=\"colData1\">"+  "<a href=\""+data.result['EntidadesDesambiguadas'][i]['dbpediaResource'] +"\" >DBpedia</a> "+ "</td>";
                }else{
                    rst += "<td  class=\"colData1\"></td><td  class=\"colData1\"></td>"
                }

                rst += "</tr>";
            }
            rst += "</table>"
            rst += "</div>"
            return rst;              
        }

        function Metadata(data, funcion) {
            var rstUp = "<div><table id = \"rstUp\"  style=\"margin: auto;\"> "
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

        function HeadMenu(funcion) {
            var rstUp = "<span class=\"menu\"><ul>"

               if (funcion == 1)
                {
                    rstUp += "<li><a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a></li>"
                } else if (funcion == 2)
                {
                    rstUp += "<li><a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a></li>"
                    
                } else if (funcion == 3)
                {
                    rstUp += "<li><a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion3')\" href=\"#\" title=\"Opción 3\" class=\"\">Etiquetas PartofSpeech)</a></li>"
                   
                } else if (funcion == 4)
                {
                    rstUp += "<li><a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion3')\" href=\"#\" title=\"Opción 3\" class=\"\">Etiquetas PartofSpeech)</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion4')\" href=\"#\" title=\"Opción 4\" class=\"\">Extración</a></li>"
                
                } else if (funcion == 5)
                {
                    rstUp += "<li><a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion3')\" href=\"#\" title=\"Opción 3\" class=\"\">Etiquetas PartofSpeech)</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion4')\" href=\"#\" title=\"Opción 4\" class=\"\">Extración</a></li>"
                    rstUp += "<li><a onclick=\"present(this,'#opcion5')\" href=\"#\" title=\"Opción 5\" class=\"\">Enlace</a></li>"
                    
                }
                rstUp += "<li><a id= \"verJson\" onclick=\"present(this,'#json')\" href=\"#\" title=\"Opción 6\" class=\"\">Json</a></li>"
                rstUp += "</ul></span>"
                return rstUp
        }

        function HeadMenu2(funcion) {


            var rstUp = "<section class=\"color-1\">"
            rstUp += "<nav class=\"cl-effect-1\">"
                

               if (funcion == 1)
                {
                    rstUp += "<a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a>"
                    
                } else if (funcion == 2)
                {
                    rstUp += "<a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a>"
                    
                    
                } else if (funcion == 3)
                {
                    rstUp += "<a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion3')\" href=\"#\" title=\"Opción 3\" class=\"\">Etiquetas PartofSpeech)</a>"
                    
                   
                } else if (funcion == 4)
                {
                    rstUp += "<a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion3')\" href=\"#\" title=\"Opción 3\" class=\"\">Etiquetas PartofSpeech)</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion4')\" href=\"#\" title=\"Opción 4\" class=\"\">Extración</a>"
                
                } else if (funcion == 5)
                {
                    rstUp += "<a onclick=\"present(this,'#opcion1')\" href=\"#\" title=\"Opción 1\" class=\"aqui\">Sentencias»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion2')\" href=\"#\" title=\"Opción 2\" class=\"\">Tokens»</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion3')\" href=\"#\" title=\"Opción 3\" class=\"\">Etiquetas PartofSpeech)</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion4')\" href=\"#\" title=\"Opción 4\" class=\"\">Extración</a>"
                    rstUp += "<a onclick=\"present(this,'#opcion5')\" href=\"#\" title=\"Opción 5\" class=\"\">Enlace</a>"
                    
                }
                rstUp += "<a id= \"verJson\" onclick=\"present(this,'#json')\" href=\"#\" title=\"Opción 6\" class=\"\">Json</a>"
                

                rstUp += "</nav></section>"
                return rstUp
        }


        function llamaServicio(servicio, funcion){
            $.getJSON($SCRIPT_ROOT + servicio, {
            text: $('textarea#textMain').val()
            }, function(data) {
                if ('err' in data.result){
                    alert(data.result['err'])    
                     var rst = "<div class = \"contenido\" >error: "+data.result['err']+" </div>";
                     var rstUp = ""
                }else{
                    var rst = "<div class = \"contenido\" >";
                    rst += "<div id = \"contenido_pestanas\" style=\"margin: auto;\">";
                    rst += HeadMenu2(funcion);
                    var rstUp = ""
                    if (funcion == 1)
                    {
                        rst+= Sentencias(data);
                    } else if (funcion == 2)
                    {
                        rst += wordTokens(data);
                        rst += Sentencias(data);
                    } else if (funcion == 3)
                    {
                        rst += Etiquetado(data);
                        rst += wordTokens(data);
                        rst += Sentencias(data);
                    } else if (funcion == 4)
                    {
                        rst += ExtracionEyK(data);
                        rst += Etiquetado(data);
                        rst += wordTokens(data);
                        rst += Sentencias(data);
                    } else if (funcion == 5)
                    {                    
                        rst += Enlace(data);
                        rst += ExtracionEyK(data);
                        rst += Etiquetado(data);
                        rst += wordTokens(data);
                        rst += Sentencias(data);
                    }
                    rstUp = Metadata(data, funcion)
                    
                    rst += "<div id=\"json\" style=\"position: absolute; display: none;\"> <textarea id=\"tjson\" rows=\"11\" cols=\"85\"  readonly> </textarea> </div>  ";
                    rst += "</div>"
                    rst += "</div>"
                }
                    ColocarHtml(rst,rstUp);
                    $('a#verJson').bind('click', function() {
                    document.getElementById("tjson").innerHTML = JSON.stringify(data);
                    });
                
            });
        }
        
        -->        
        var rst = "<div class=\"spinner\"> "+
              "<div class=\"spinner-container container1\"> " +
                "<div class=\"circle1\"></div> " +
                "<div class=\"circle2\"></div> " +
                "<div class=\"circle3\"></div> " +
                "<div class=\"circle4\"></div> " +
              "</div> " +
              "<div class=\"spinner-container container2\"> " +
                "<div class=\"circle1\"></div> " +
                "<div class=\"circle2\"></div> " +
                "<div class=\"circle3\"></div> " +
                "<div class=\"circle4\"></div> " +
              "</div> " +
              "<div class=\"spinner-container container3\"> " +
                "<div class=\"circle1\"></div> " +
                "<div class=\"circle2\"></div> " +
                "<div class=\"circle3\"></div> " +
                "<div class=\"circle4\"></div> " +
              "</div> " +            "</div>" 

        
        
        var rstUp = "<div class=\"spinner\">  <div class=\"bounce1\"></div>  <div class=\"bounce2\"></div>  <div class=\"bounce3\"></div> </div>"
        rstUp = ""




        ColocarHtml(rst, rstUp)

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

