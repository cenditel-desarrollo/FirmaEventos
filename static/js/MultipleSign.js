


function True_FalseMultiples(data){

    if (data == "true" ){
      return "Verdadero";
    }
    if (data ==  "false"){
      return "Falso";
    }

}

function SerealizeMyJsonMultiples(data){
  for (var i = 0; i < data.signatures.length; i++) {
      data.signatures[i].integrityCheck = True_FalseMultiples(data.signatures[i].integrityCheck);
      data.signatures[i].signerCertificateStillValid = True_FalseMultiples(data.signatures[i].signerCertificateStillValid);
      data.signatures[i].signerCertificateValidAtTimeOfSigning = True_FalseMultiples(data.signatures[i].signerCertificateValidAtTimeOfSigning);
      data.signatures[i].signatureCoversWholeDocument = True_FalseMultiples(data.signatures[i].signatureCoversWholeDocument);
      data.signatures[i].certificatesVerifiedAgainstTheKeyStore = True_FalseMultiples(data.signatures[i].certificatesVerifiedAgainstTheKeyStore);         
  }
  return data;
}


//Obtenemos la  informacion de documento
function InfoDocumentDataTablePDFMultiples(signedFileId){

    $.ajax({
        //url: "https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/"+signedFileId,
        url: "https://192.168.12.154:8443/Murachi/0.1/archivos/"+signedFileId,
        type: "get",
        dataType: "json",        
        headers: {"Authorization":"Basic YWRtaW46YWRtaW4="},
        success: function(response) {
            
	  		
	        INFO_DATATABLE_MULTIPLES = SerealizeMyJsonMultiples(response);
			
			CONT_MULTIPLES += 1;
			if (CONT_MULTIPLES == 1){
				DATATABLE_SIGN_MULTIPLES = DataTablePDFMultiples(response);	

			}
			if (CONT_MULTIPLES > 1){
				DATATABLE_SIGN_MULTIPLES.destroy();
				DATATABLE_SIGN_MULTIPLES = DataTablePDFMultiples(response);	
			}	


			$("#Cuerpo_Sign").hide();
			$("#Cuerpo_check").hide();
			$("#well_mensaje").hide();
			$("#button_SignMultiples").hide();
			$("#myJsonPDFMultiples_wrapper").show();	
			ListarDocument()				


			
        },
        error: function(jqXHR, textStatus, errorThrown){
          	alert(textStatus+", "+ errorThrown+" el documento PDF para mostrar la info de la sign");     
        }
	});
}


// Cuarto paso (Se envia la información del token para terminar la firma)
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

			//var linkToDownload = "<a href=\"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/descargas/" + data['signedFileId'] +"\"><h4>Descargar archivo firmado</h4></a>";
			var linkToDownload = "<a href=\"https://192.168.12.154:8443/Murachi/0.1/archivos/descargas/" + data['signedFileId'] +"\"><h4>Descargar archivo firmado</h4></a>";
			document.getElementById("log").innerHTML = '';   
			document.getElementById("respuesta").innerHTML = '<center><h2>Archivo firmado correctamente:</h2> <br>'+linkToDownload+'</center>';  			

			InfoDocumentDataTablePDFMultiples(data['signedFileId']);		

		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('error en pdfs/resenas: ' + textStatus);
			$("#respuesta").html("error en pdfs/resenas: " + textStatus);
		}
	});

}


//Tercer paso (Obtenemos el hash de pdf enviado por el servidor y luego procesa la información en el token)
function ObtenerHashPDFServerMultiples(parameters,cert){

	$.ajax({
		type: 'POST',
		contentType: 'application/json',				
		url:"https://192.168.12.154:8443/Murachi/0.1/archivos/pdfs2",
		//url:"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/pdfs",
		dataType: "json",
		data: parameters,		
		xhrFields: {withCredentials: true},
		headers: {"Authorization":"Basic YWRtaW46YWRtaW4="},
		success: function(data, textStatus, jqXHR){
			var json_x = data;
			var hash = json_x['hash']; 
			//alert("hash recibido del servidor "+hash);		
			var hashtype = "SHA-256";
			var lang = "eng";
			
			//Procesa la información
			window.hwcrypto.sign(cert, {type: hashtype, hex: hash}, {lang: lang}).then(
				function(signature) {
					FinalizarFirmaMultiples(signature.hex);
      			}, 
      			function(err) {
	        		log_text("sign() failed: " + err);
					var error;
                    log_text("sign() failed: " + err);
                    if(err == "Error: user_cancel") {
                        alert("sign() failed: El usuario cancelo la operación");
                        error = "El usuario cancelo la operación"; 
                     }      
                     else if(err == "Error: no_certificates") {
                         alert("sign() failed: No hay certificado disponible");
                         error = "No hay certificado disponible";
                     }
                     else if(err == "Error: no_implementation") {
                         alert("sign() failed: No hay soporte para el manejo del certificado");
                         error = "No hay soporte para el manejo del certificado";
                     }

	        		//alert("sign() failed: " + err);
	        		$("#respuesta").html("sign() failed: " + error);
    	  	});
			
		},								
		error: function(jqXHR, textStatus, errorThrown){
			//alert('error: ' + textStatus);
			//var responseText = jQuery.parseJSON(jqXHR.responseText);
			alert('ajax error function: ' + jqXHR.responseText);
			$("#respuesta").html("error function: " + jqXHR.responseText);
		}
		
	});
		
}


//Segundo paso (Seleccionamos el Certificado Firmante)
function ObtenerCertificadoFirmanteMultiples(fileId){

	// identificador del archivo en el servidor
	

	window.hwcrypto.getCertificate({lang: "en"}).then(
		function(response) {
	  		var cert = response;
	  		console.log(response);
	  		console.log("ssss");
	  		var parameters = "";
			parameters = JSON.stringify({
				"fileId":fileId,
				"certificate":cert.hex,
				"reason":"Certificado",
				"location":"CENDITEL",
				"contact":"582746574336",
				"signatureVisible":"false",
				"signaturePage": "",
				"xPos": "",
				"yPos": ""
				});				

			// ahora llamar al ajax de obtener la resena del pdf
			ObtenerHashPDFServerMultiples(parameters, cert);	

		}, 
		function(err) {
  			log_text("getCertificate() failed: " + err);
            var error;
            if(err == "Error: user_cancel") {
                alert("getCertificate() failed: El usuario cancelo la operación"    );
                error = "El usuario cancelo la operación"; 
             }      
             else if(err == "Error: no_certificates") {
                 alert("getCertificate() failed: No hay certificado disponible")    ;
                 error = "No hay certificado disponible";
             }
             else if(err == "Error: no_implementation") {
                 alert("getCertificate() failed: No hay soporte para el manejo del certificado");
                 error = "No hay soporte para el manejo del certificado";
			}
  			//alert("getCertificate() failed: " + err);
  			$("#respuesta").html("getCertificate() failed: " + error);
		}

	);
}


function ListarDocument(){


	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url:"https://192.168.12.154:8443/Murachi/0.1/archivos/listado",
		//url:"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/pdfs/resenas",
        type: "get",
        dataType: "json",        
        headers: {"Authorization":"Basic YWRtaW46YWRtaW4="},
		success: function(response, textStatus, jqXHR){

			
			var options = "";
			options += '<option value="-1"> Seleccionar </option>';			
			for (var i = 0; i < response.murachiWorkingDirectoryContent.length; i++)
			{ 
				var data =  response.murachiWorkingDirectoryContent[i].split(".");
				if ( data.length > 1 && data[1] ==  "pdf"){
					 options += '<option value="'+response.murachiWorkingDirectoryContent[i]+'" title ="'+response.murachiWorkingDirectoryContent[i]+'">' +response.murachiWorkingDirectoryContent[i] +'</option>';
				}
			}

			$('#listadoDocument').html(options);
			$('#listadoDocument option:first').attr('selected', 'selected');
			$("#SelectArchivos").show();

		},
		error: function(jqXHR, textStatus, errorThrown){
			alert('error en pdfs/resenas: ' + textStatus);
			$("#respuesta").html("error en pdfs/resenas: " + textStatus);
		}
	});


}


$("#button_ListarMultiples").on('click', function() {	
	ListarDocument();
});

$("#listadoDocument").on('click', function() {
	var fileId = $("#listadoDocument").val();

	if (fileId != -1 ) {
			$("#button_SignMultiples").show();
	}
	else{
			$("#button_SignMultiples").hide();
	}



});



$("#Form_sign_multiples").on('submit', function(event) {
	event.preventDefault();
	
	var fileId = $("#listadoDocument").val();

	if (fileId != -1 ) {
		ObtenerCertificadoFirmanteMultiples(fileId);
	}
	else{
		alert("Debe selecionar un documeto");
	}

	
});

