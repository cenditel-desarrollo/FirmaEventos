

var __PDF_DOC,
  __CURRENT_PAGE,
  __TOTAL_PAGES,
  __PAGE_RENDERING_IN_PROGRESS = 0,
  __CANVAS = $('#pdf-canvas2').get(0),
  __CANVAS_CTX = __CANVAS.getContext('2d'),
  __id = "",
  __NUMBER = 0,
  __CLICK = 0;

 $("#pdf-canvas2").hide();
function showPDF2(pdf_url) {
  $("#pdf-loader2").show();

  PDFJS.getDocument({ url: pdf_url }).then(function(pdf_doc) {
    __PDF_DOC = pdf_doc;
    __TOTAL_PAGES = __PDF_DOC.numPages;
    
    // Hide the pdf loader and show pdf container in HTML
    $("#pdf-loader2").hide();
    $("#pdf-contents2").show();
    $("#pdf-total-pages2").text(__TOTAL_PAGES);

    // Show the 
      showPage2(1);
  
  }).catch(function(error) {
    // If error re-show the upload button
    $("#pdf-loader2").hide();
    $("#upload-button2").show();
    
    alert(error.message);
  });;
}

function showPage2(page_no) {
  __PAGE_RENDERING_IN_PROGRESS = 1;
  __CURRENT_PAGE = page_no;

  // Disable Prev & Next buttons while page is being loaded
  $("#pdf-next2, #pdf-prev2").attr('disabled', 'disabled');

  // While page is being rendered hide the canvas and show a loading message
  $("#pdf-canvas2").hide();
  $("#page-loader2").show();

  // Update current page in HTML
  $("#pdf-current-page2").text(page_no);
  
  VALOR_PAGE = page_no;
  
  // Fetch the page
  __PDF_DOC.getPage(page_no).then(function(page) {
    // As the canvas is of a fixed width we need to set the scale of the viewport accordingly


    var scale_required = __CANVAS.width / page.getViewport(1).width;

    // Get viewport of the page at required scale
    var viewport = page.getViewport(scale_required);

    // Set canvas height

    __CANVAS.height = viewport.height;


    var renderContext = {
      canvasContext: __CANVAS_CTX,
      viewport: viewport
    };


    // Render the page contents in the canvas
    page.render(renderContext).then(function() {
      __PAGE_RENDERING_IN_PROGRESS = 0;

      // Re-enable Prev & Next buttons
      $("#pdf-next2, #pdf-prev2").removeAttr('disabled');

      // Show the canvas and hide the page loader
      $("#page-loader2").hide();

        __id = __CANVAS.toDataURL()
       
      var viewdimen = page.getViewport(1);  

      $("#container1").attr("style", "background-image: url('"+__id+"');background-size: cover; background-repeat: no-repeat;  height:"+viewdimen.height+"px; width:"+viewdimen.width+"px");      


    });
  });


}

// Upon click this should should trigger click on the #file-to-upload file input element
// This is better than showing the not-good-looking file input element
$("#file").on('click', function() {
  
  $("#pdf-main-container").show();
  CONTAINER = true;
  $("#file").trigger('click');

});

// When user chooses a PDF file
$("#file").on('change', function() {

  // Validate whether PDF
  if(['application/pdf'].indexOf($("#file").get(0).files[0].type) == -1) {
      alert('Error : Not a PDF');
      return;
  }


  if (__CLICK == 0){
      $('#firmar-documento').attr("disabled","disabled").show();
      $('#texto').show();
      __CLICK += 1;
  }
  else{

    $("#texto").hide();
    $('#firmar-documento').show();
  }

  // Send the object url of the pdf
  showPDF2(URL.createObjectURL($("#file").get(0).files[0]));




});

// Previous page of the PDF
$("#pdf-prev2").on('click', function() {
  if(__CURRENT_PAGE != 1)
    showPage2(--__CURRENT_PAGE);
});

// Next page of the PDF
$("#pdf-next2").on('click', function() {
    

  if(__CURRENT_PAGE != __TOTAL_PAGES)
    
    showPage2(++__CURRENT_PAGE);

});


