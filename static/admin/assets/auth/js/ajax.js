$(document).ready(function() {
//Ajax login form Login
  const login = $('form#login.form')
  login.on('submit', function(e){
    e.preventDefault();
       ajaxforms('/login', 'POST', $(this));
       });

//Registration Ajax
  const regForm = $('form#register');  
  regForm.on('submit', function(e){
    e.preventDefault();
    ajaxforms('/register', 'POST', $(this));
  });


//Lock screen
$('#lockForm').on('submit', function(e){
  e.preventDefault();
  const form = $(this);
  
  if(form.find('input[name="password"]').val() != ''){
    ajaxforms('/lock', 'POST', form)
  }
  else{
    noMatch(form)
  }
})

    function ajaxforms(url, type, form){
      $.ajax({
        url: url,
        type: type,
        data: $(form).serialize()
      })
      .done(function(response){
        let callback = eval(response.callback)
        if(response.param){
          if(response.param == 'form'){
            callback = callback(form)
          }
          else{
            callback = callback(response.param)
          }
        }
        Swal.fire({
          type: response.alertType,
          text: response.message,
          timer: response.timer,
          onClose: callback
        })
        
      })
    }

    function goToRegister(){
        window.location.href = '/register';
    }
    function goToAdmin(){
      window.location.href='/admin';
    }
    function goToLogin(){
      window.location.href ='/login';
    }
    function clearPassFields(){
      $(document.querySelectorAll('input[type="password"]')).each(function(){$(this).val("");})    
    }
    function clearEmailFields(){
      $(document.querySelectorAll('input[type="email"]')).each(function(){$(this).val("");})
    }
    function unlock(url){
      window.location.href= url;
    }

    function noMatch(form){
      form.parent().parent().addClass('animated shake');
      setTimeout(function(){
        form.parent().parent().removeClass('animated shake');
      }, 1000);
    }
});