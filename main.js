$(function(){
  //
  $("#btn").click(function(){
     domtoimage.toBlob(document.getElementById('table'))
        .then(function (blob) {
            var model = $('.model').text()
            // window.saveAs(blob, 'scorecard.png');
            window.saveAs(blob,  model + '_scorecard.png');
        });
  })

  

$("#legend_btn").click(function() {
    $('.legend_show').slideToggle('fast');
  });
});
