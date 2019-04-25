$(document).ready(function() {
$(function () {
  //initalize all tooltips
    // $('[data-toggle="tooltip"]').tooltip()
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
    //remove place holder on focus
    const titlebox = document.querySelector('#addPostTitle');
    const contentbox = document.querySelector('#contentbox');
    let s = window.getSelection(), r = document.createRange();
    const toolsbar = document.querySelector('#toolbar');

    r.setStart(titlebox, 0);
    r.setEnd(titlebox, 0);
    s.removeAllRanges();
    s.addRange(r);
 
  // Create WYSIWYG functions for rich text editors
  $('.tools a').mousedown(function(e){
    e.preventDefault();
    let command = $(this).data('command');
    if(command == 'bold' || command == 'underline' || command == 'strikeThrough' || command == 'superscript'){
      $(this).parent().toggleClass('active');
    }
    if(command == 'foreColor' || command == 'insertImage' || command == 'heading' || command == 'fontSize' || command == 'fontName'){
      // let $this = $(this)
      $(this).next().children('input').trigger('click');
      let input = $(this).next().children();
      console.log(input);      
     input.on('change', function(e){
        let val = $(input).val();
        console.log(val);
        document.execCommand(command, false, val);
      })
    }
    if (command == 'h1' || command == 'h2' || command == 'p') {
      document.execCommand('formatBlock', false, command);
    }
    // if (command == 'foreColor' || command == 'backcolor') {
    //   document.execCommand($(this).data('command'), false, $(this).data('value'));
    //   console.log($(this).children('input').val());
      
    // }
    if (command == 'createlink') {
      url = prompt('Enter the link here: ', 'http:\/\/');
      document.execCommand($(this).data('command'), false, url);
    } 
    else document.execCommand($(this).data('command'), false, null);
   
    });



  
   


  });

});