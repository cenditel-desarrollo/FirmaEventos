/**
 * Funcion para refrescar el captcha
 * @param element Recibe el parametro
*/

function refresh_captcha(element) {
    $form = $(element).parents('form');
    var url = location.protocol + "//" + window.location.hostname + ":" + location.port + "/captcha/refresh/";

    $.getJSON(url, {}, function(json) {
        $form.find('input[name="captcha_0"]').val(json.key);
        $form.find('img.captcha').attr('src', json.image_url);
    });

    return false;
}

/**
 * Función para obtener los usuarios de un evento
*/
function get_event_user() {
    var modal = false;
    var pasaporte = $('#id_pasaporte').val();
    if (pasaporte!='') {
        var routes = $(location).attr('pathname').split('/');
        var pk = routes[routes.length-1];
        var url = URL_USUARIO_EVENTO+pk+"/"+pasaporte;
        $.getJSON(url, function(data){
            if (Object.keys(data).length > 0) {
                construir_datos(data.datos);
            }
            else{
                simple_modal('Lo sentimos, no esta registrado para firmar');
            }
        }).fail(function(jqxhr, textStatus, error) {
            simple_modal('Petición fállida' + textStatus + ", " + error);
        })
    }
    else{
        simple_modal('Debe ingresar un pasaporte');
    }    
}

/**
 * Función para crear un modal sencillo
*/
function simple_modal(mensaje) {
    MaterialDialog.alert(
        mensaje,
        {
            title:'Alerta',
            buttons:{
                close:{
                    text:'cerrar',
                    className:'blue',
                }
            }
        }
    );
}

/**
 * Función para construir la data del participante
 * @param data Recibe los datos para crear la lista
*/
function construir_datos(data) {
    $('#datos_paricipante').html('');
    html = '<ul class="collection">'
    html += '<li class="collection-item"><b>Nombre: </b>'+data.nombres+'</li>';
    html += '<li class="collection-item"><b>Apellido: </b>'+data.apellidos+'</li>';
    html += '<li class="collection-item"><b>Pasaporte: </b>'+data.pasaporte+'</li>';
    html += '<li class="collection-item"><b>Correo: </b>'+data.correo+'</li>';
    html += '</ul>';
    html += '<iframe width="700px" height="600px" src="https://192.168.12.154:8443/Murachi/0.1/archivos/listadopdf/cbcd0924-bbfe-49dc-afc8-f32348f20350.pdf">';
    html += '</iframe><br/>';
    html += '<a type="button" class="btn waves-effect blue darken-1" onclick="ObtenerCertificadoFirmanteMultiples(\''+data.documento+'\')">';
    html += '<i class="material-icons left">mode_edit</i> Firmar</a>';
    $('#datos_paricipante').html(html);
}