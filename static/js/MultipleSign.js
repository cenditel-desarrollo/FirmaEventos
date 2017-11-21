// Cuarto paso (Se envia la información del token para terminar la firma)
function FinalizarFirmaMultiples(signature){

	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		//url:"https://192.168.12.154:8443/Murachi/0.1/archivos/pdfs/resenas",
		url:"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/pdfs/resenas",
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
		//url:"https://192.168.12.154:8443/Murachi/0.1/archivos/pdfs2",
		url:"https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/pdfs",
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
				"contact":"RedGealc",
				"signatureVisible":"false",
				"signaturePage": "",
				"xPos": "",
				"yPos": ""
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
}

