$(function(){
  //
  $("#btn").click(function(){
     domtoimage.toBlob(document.getElementById('table'))
        .then(function (blob) {
            window.saveAs(blob, 'scorecard.png');
        });
  })


$("#legend_btn").click(function() {
    $('.legend_show').slideToggle('fast');
  });
});
