$(document).ready(function() {
$(function () {
  //initalize all tooltips
    $('[data-toggle="tooltip"]').tooltip();
    $('.nav-mobile-menu .nav-item a.nav-link').removeClass('btn', 'btn-white', 'btn-round');
  window.onresize = navLink;
  
  // create mobile view for the navbar
  function navLink(){
    if(window.innerWidth < 991){
      $('.nav-mobile-menu .nav-item a.nav-link').removeClass('btn', 'btn-white', 'btn-round');
    }
  }
  
  //initate date picker for event posts
  $('.datetimepicker').datetimepicker({
    icons: {
        time: "fa fa-clock-o",
        date: "fa fa-calendar",
        up: "fa fa-chevron-up",
        down: "fa fa-chevron-down",
        previous: 'fa fa-chevron-left',
        next: 'fa fa-chevron-right',
        today: 'fa fa-screenshot',
        clear: 'fa fa-trash',
        close: 'fa fa-remove'
    }
 });

 //Set cursor focus of contenteditable elements
     const titlebox = document.querySelector('#addPostTitle');
    const contentbox = document.querySelector('#contentbox');
    let s = window.getSelection(), r = document.createRange();
    let editDiv;

  //Set caret to beginning of title box
    r.setStart(titlebox, 0);
    r.setEnd(titlebox, 0);
    s.removeAllRanges();
    s.addRange(r);

  //Save selection ranges
   savedRanges = new Object();
$('div[contenteditable="true"]').focus(function(){
    var s = window.getSelection();
    var t = $('div[contenteditable="true"]').index(this);
    if (typeof(savedRanges[t]) === "undefined"){
        savedRanges[t]= new Range();
    } else if(s.rangeCount > 0) {
        s.removeAllRanges();
        s.addRange(savedRanges[t]);
    }
}).bind("mouseup keyup",function(){
    var t = $('div[contenteditable="true"]').index(this);
    savedRanges[t] = window.getSelection().getRangeAt(0);
}).on("mousedown click",function(e){
    if(!$(this).is(":focus")){
        e.stopPropagation();
        e.preventDefault();
        $(this).focus();
    }
});
  

    //Get the last active contenteditable div

    window.addEventListener('keyup', function(e){
      if(document.activeElement == titlebox){
            editDiv = titlebox;
      }
      if(document.activeElement == contentbox){
        editDiv = contentbox;
      }     
  });  

    window.addEventListener('mouseup', function(e){
      if(document.activeElement == titlebox){
        editDiv = titlebox;
      }
      if(document.activeElement == contentbox){
        editDiv = contentbox;
      }
  });
  
  //Place Caret at the end of the text
  function placeCaretAtEnd(el) {
    el.focus();
    if (typeof window.getSelection != "undefined"
            && typeof document.createRange != "undefined") {
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    } else if (typeof document.body.createTextRange != "undefined") {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.collapse(false);
        textRange.select();
    }
}

     
  // Create WYSIWYG functions for rich text editors
  $('.tools a').mousedown(function(e){
    e.preventDefault();
    let command = $(this).data('command');
    if(command == 'bold' || command == 'underline' || command == 'strikeThrough' || command == 'superscript'){
    }
    if(command == 'backColor' || command == 'foreColor'){
      $(this).next().children('input').trigger('click');
        let input = $(this).next().children();      
        input.on('change', function(e){
        let val = $(input).val();
        document.execCommand(command, false, val);
      })
    }
    else if(command == 'heading'){
      $(this).parent().addClass('active');
      let headings = $(this).next().find('select');
       headings.on('change', function(e){
         let val = event.target.value;
         document.execCommand('formatBlock', false, val);
        $(this).parent().parent().prev().parent().removeClass('active');
       });
    }
    if (command == 'fontSize' || command == 'fontName') {
        $(this).parent().addClass('active');
        let com = $(this).next().find('select');
        com.on('click change', function(e){
        let val = e.target.value;     
        document.execCommand(command, false, val);
        $(this).parent().parent().prev().parent().removeClass('active');
      })   
    }
    else if (command == 'createlink') {
      url = prompt('Enter the link here: ', 'http:\/\/');
      document.execCommand($(this).data('command'), false, url);
    } 
    else if(command == 'insertImage'){
      $("#uploadsGallery").modal();
      $('.ftco-animate').addClass('fadeInUp ftco-animated')
      let check = $(this).next().find('input.form-check-input');
      let val;
	    check.on('change', function(e){
       val = $(this).val();          
      });     
      $('#insertImg').unbind('click').click(function (e) {
        placeCaretAtEnd(editDiv);
        document.execCommand(command, false, val);
        check.prop('checked',  false);
        placeCaretAtEnd(editDiv);        
      });
    }
    else
    {
      document.execCommand($(this).data('command'), false, null);
      } 
    });



  
   


  });

});