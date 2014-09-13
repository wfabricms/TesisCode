
  $(document).ready(function(){ // Script del Navegador
    $('#contenido_pestanas div').css('position', 'absolute').not(':first').hide();
    $('#contenido_pestanas ul li:first a').addClass('aqui');
    $('#contenido_pestanas a').click(function(){
        $('#contenido_pestanas a').removeClass('aqui');
        $(this).addClass('aqui');
        $('#contenido_pestanas div').fadeOut(350).filter(this.hash).fadeIn(350);
        return false;
        
    });
 });


function presenta2() {
	//$('#contenido_pestanas div').css('position', 'absolute').not(':first').hide();
    //$('#contenido_pestanas ul li:first a').addClass('aqui');

    $('#contenido_pestanas a').removeClass('aqui');
        $(this).addClass('aqui');
        $('#contenido_pestanas div').fadeOut(350).filter(this.hash).fadeIn(350);
        return false;
  }