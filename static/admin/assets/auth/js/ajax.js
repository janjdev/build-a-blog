$(document).ready(function() {
//Ajax login form

  const login = $('form#login.form')
  login.on('submit', function(e){
       $.ajax({
          url: '/login',
          type: 'POST',
          data: $(this).serialize()
       })
      .done(function(resp){
                if (resp.error){
                  if(resp.error == 1){
                    Swal.fire({
                      type: resp.alertType,
                      text: resp.message,
                      timer: 5000,
                    }).then(result => {
                        if(result.value){
                    login.find('input[name="email"]').val("");
                    login.find('input[name="password"]').val("")
                        }
                    })
                  }else
                    if(resp.error == 2){
                    Swal.fire({
                        position: 'top-end', 
                        type: resp.alertType,
                        title: resp.message,
                        showConfirmButton: true,
                        timer: 5000,
                        onClose: goToRegister,                
                    });
                    // .then(result => {
                    //     if(result.value){
                    //         window.location.replace('/register');
                    //     }
                    // })
                  }
                    else{
                        Swal.fire({
                        text: resp.message,
                        type: resp.alertType,
                        })
                    }              
                
                }
                if(resp.sucess == 2){
                  Swal.fire({
                    type: resp.alertType,
                    timmer: 5000
                  }).then(result  => {
                      if(result.value){
                    window.location.replace('/admin')
                      }
                  })
                }else{
                     //e.stopPropogation();               
              //window.location.replace('/admin')
                }
              
             
           });
           e.preventDefault();
       });
    function goToRegister(){
        window.location.href = 'register';
    }
});