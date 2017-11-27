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
                construir_datos(data);   
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
    firma = data.firmo;
    data = data.datos;
    $('#datos_paricipante').html('');
    html = '<ul class="collection">'
    html += '<li class="collection-item"><b>Nombre: </b>'+data.nombres+'</li>';
    html += '<li class="collection-item"><b>Apellido: </b>'+data.apellidos+'</li>';
    html += '<li class="collection-item"><b>Pasaporte: </b>'+data.pasaporte+'</li>';
    html += '<li class="collection-item"><b>Correo: </b>'+data.correo+'</li>';
    html += '</ul>';
    html += '<iframe width="700px" height="600px" src="https://192.168.12.154:8443/Murachi/0.1/archivos/listadopdf/'+data.documento+'">';
    html += '</iframe><br/>';
    if (firma==true) {
        html += '<h4 class="red-text center">Ya firmó este documento</h4>'
    }
    else{
        html += '<a type="button" id="firmar" class="btn waves-effect blue darken-1" onclick="ObtenerCertificadoFirmanteMultiples(\''+data.documento+'\')">';
        html += '<i class="material-icons left">mode_edit</i> Firmar</a>';   
    }
    $('#datos_paricipante').html(html);
}

/**
 * Función para obtener el certificado del participante
 * @param fileId Recibe el id del documento
*/
function ObtenerCertificadoFirmanteMultiples(fileId){
    var xPos = yPos= signaturePage = "";
    var lastSignature = false;
    var routes = $(location).attr('pathname').split('/');
    var pk = routes[routes.length-1];
    
    $.ajax({
		type: 'GET',
        async: false,
		url:URL_ULTIMO_FIRMANTE+pk,
		success: function(datos){
            if (datos.valid==true) {
                xPos = datos.data.posX;
                yPos = datos.data.posY;
                signaturePage = datos.data.page;
                lastSignature = true;
            }
            window.hwcrypto.getCertificate({lang: "en"}).then(
                function(response) {
                    var cert = response;
                    var parameters = "";
                    parameters = JSON.stringify({
                        "fileId":fileId,
                        "certificate":cert.hex,
                        "reason":"Certificado",
                        "location":"RedGealc",
                        "contact":"RedGealc",
                        "signatureVisible":"false",
                        "signaturePage": signaturePage,
                        "xPos": xPos,
                        "yPos": yPos,
                        "lastSignature":lastSignature
                        });				
        
                    // ahora llamar al ajax de obtener la resena del pdf
                    ObtenerHashPDFServerMultiples(parameters, cert);	
        
                }, 
                function(err) {
                    var error;
                    if(err == "Error: user_cancel") {
                        error = "El usuario cancelo la operación"; 
                     }      
                     else if(err == "Error: no_certificates") {
                         error = "No hay certificado disponible";
                     }
                     else if(err == "Error: no_implementation") {
                         error = "No hay soporte para el manejo del certificado";
                    }
                    simple_modal(error);
                }
        
            );
		},
		error: function(jqXHR, textStatus, errorThrown){
			console.log('error: ' + textStatus);
		}
	});
}


/**
 * Función para obtener el hash y procesar la informacion
 * @param parameters Recibe los parametros
 * @param cert Recibe los certificados
*/
function ObtenerHashPDFServerMultiples(parameters,cert){

	$.ajax({
		type: 'POST',
		contentType: 'application/json',				
		url:"https://192.168.12.154:8443/Murachi/0.1/archivos/pdfs2",
		//url:"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/pdfs",
        //url: "https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/firmados/pdfs",
		dataType: "json",
		data: parameters,		
		xhrFields: {withCredentials: true},
		headers: {"Authorization":"Basic YWRtaW46YWRtaW4="},
		success: function(data, textStatus, jqXHR){
			var json_x = data;
			var hash = json_x['hash']; 		
			var hashtype = "SHA-256";
			var lang = "eng";
			
			//Procesa la información
			window.hwcrypto.sign(cert, {type: hashtype, hex: hash}, {lang: lang}).then(
				function(signature) {
					FinalizarFirmaMultiples(signature.hex);
      			}, 
      			function(err) {
					var error;
                    if(err == "Error: user_cancel") {
                        error = "El usuario cancelo la operación"; 
                     }      
                     else if(err == "Error: no_certificates") {
                         error = "No hay certificado disponible";
                     }
                     else if(err == "Error: no_implementation") {
                         error = "No hay soporte para el manejo del certificado";
                     }
                    simple_modal(error);
    	  	});
			
		},								
		error: function(jqXHR, textStatus, errorThrown){
			console.log('ajax error function: ' + jqXHR.responseText);
		}
		
	});	
}

/**
 * Función para enviar la firma al servidor
 * @param signature Recibe la firma
*/
function FinalizarFirmaMultiples(signature){

	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url:"https://192.168.12.154:8443/Murachi/0.1/archivos/pdfs/resenas",
		//url:"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/pdfs/resenas",
		dataType: 'json',
		data: JSON.stringify({"signature":signature}),
		xhrFields: {withCredentials: true},
		headers: {"Authorization":"Basic YWRtaW46YWRtaW4="},
		success: function(data, textStatus, jqXHR){
            actualizar_participante(data['signedFileId']);
		},
		error: function(jqXHR, textStatus, errorThrown){
			console.log('error en pdfs/resenas: ' + textStatus);
		}
	});

}

/**
 * Función para actualizar los datos del participante
 * @param id_documento Recibe el id del documento
*/
function actualizar_participante(id_documento) {
    var pasaporte = $('#id_pasaporte').val();
    var routes = $(location).attr('pathname').split('/');
    var pk = routes[routes.length-1];
    
    $.post(URL_ACTUALIZAR_PARTICIPACION,{'event_id':pk,'pasaporte':pasaporte,'serial':id_documento})
    .done(function(data){
        if (data.validate==true) {
            simple_modal(data.mensaje);
            $('#firmar').remove();
        }
        else{
            simple_modal(data.mensaje);
        }
    })
    .fail(function(err){
        console.log(err);
    });
}
