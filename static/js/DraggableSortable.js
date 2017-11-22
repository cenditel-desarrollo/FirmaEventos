
function InicializarObjectoPositicion(){
  var container = document.getElementById('container1'),
    element = document.getElementsByClassName('text')[0];
  
  // options
  var options = {
    limit: container,
    setCursor: true
  };

  // initialize drag
  new Draggable(element, options); 

}


function NuevoObjectoInicial(){

  var num = 0;
  $( ".text" ).draggable({ 
    containment: '#container1',
    scroll: false,
    stop: function(event, ui)
      {
       
        num+= 1;
        if (num == 1){
          $("#firma_visible #Formato_Visible .text").hide();
          console.log(VALOR_X);
          VALOR_X = 0;
          VALOR_Y = 0;
        }else{
          VALOR_X = parseInt(ui.position['left']);
          VALOR_Y = parseInt(ui.position['top']);
          console.log(VALOR_X, VALOR_Y)
        }
        $('#id_pos_x').val(VALOR_X)
        $('#id_pos_y').val(VALOR_Y)
        $('#id_pag').val(__CURRENT_PAGE)
      },
    
  });
}


var transferred = false;
$('.text').draggable({
    connectToSortable: "div#container1",
    helper: 'clone',
    start: function(event, ui)
    {
        $(this).hide();
    },
    stop: function(event, ui)
    {

        if(!transferred) {
            $(this).show();
        }
        else{ 
        
            $(this).remove();
            transferred = false;
        }
    }
});


$('div#container1').sortable({
    connectWith: "div#container1",
    receive: function(event, ui)
    { 
        transferred = true;
        $("#firmar-documento").removeAttr('disabled');
        InicializarObjectoPositicion()
        NuevoObjectoInicial();      
    }
});
