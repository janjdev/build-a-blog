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
  

 //Attach Featured Image to Post
 const attchbtn = document.querySelector('#attachmentBtn');
 if(attchbtn){
  $(attchbtn).on('click', function(e){
    $('.ftco-animate').addClass('fadeInUp ftco-animated');
        $('#imgBrowser').modal();
      let check =   $(this).parent().next().find('input.form-check-input');
      let val;
      check.on('change', function(e){
        val = $(this).val();
      });
      $('#instImg').unbind('click').click(function(e){
        $('.fileinput-preview.thumbnail img').attr('src', val);
        $('input[name="featureImg"]').attr('value', val);
      });
  });
}

const typeSel = document.getElementById('postType');
if(typeSel){
  typeSel.addEventListener('change', function(e){
    if(e.target.value == 'Event'){
      $('.input-group.animated.flipInX').css('display', 'flex');
    }
    else{
      $('.input-group.animated.flipInX').css('display', 'none');
    }
  })
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

 

  if($('div[contenteditable="true"]')){
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
  
}
    //Get the last active contenteditable div
  if(titlebox){
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

   //Set caret to beginning of title box
   r.setStart(titlebox, 0);
   r.setEnd(titlebox, 0);
   s.removeAllRanges();
   s.addRange(r);
}
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


//Bulk Actions============================================
  const  actionsCheck = document.getElementById('bulk-actions-check');
  if(actionsCheck){
    actionsCheck.addEventListener('change', function(e){
      let checks = document.getElementsByClassName('post-action');
      for(let el of checks){
        if(this.checked){
          el.checked = true;
        }else{
          el.checked = false;
        }
      }
    });
  }

 //PopOver for media galleries
 // magnific popup
 $('.image-popup').magnificPopup({
  type: 'image',
  closeOnContentClick: true,
  closeBtnInside: false,
  fixedContentPos: true,
  mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
   gallery: {
    enabled: true,
    navigateByImgClick: true,
    preload: [0,1] // Will preload 0 - before current, and 1 after the current image
  },
  image: {
    verticalFit: true
  },
  zoom: {
    enabled: false,
    duration: 300 // don't foget to change the duration also in CSS
  }
});

$('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
  disableOn: 700,
  type: 'iframe',
  mainClass: 'mfp-fade',
  removalDelay: 160,
  preloader: false,

  fixedContentPos: false
});
  
 });
 

});