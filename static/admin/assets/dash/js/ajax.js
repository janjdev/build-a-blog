// const pyUrl = 'https://www.googleapis.com/blogger/v3/blogs/8520/posts?key=AIzaSyC3N7-adc4BJmHPek_dZAClL_50ouKTbH4';
// $.ajax({
//     url:pyUrl,
//     type: 'GET',
//     contentType: "appplication/json",       
// }).done(function(resp){
//     console.log(resp);
//     $.ajax({
//         url: '/admin',
//         type: 'POST',
//         contentType: "appplication/json",
//         data: '../../../../../data/data.json',
//     }).done(function(response){
//         console.log(response);
//     });
// // });


$(document).ready(function() {
//To update userProfiles
    const form = document.querySelector('form#updateProfile');
    id = form.getAttribute('data-form-user')
    $(form).on('submit', function(e){
        e.preventDefault();
        let fields = document.querySelectorAll('.editable');
        let Empty = true;
        let i = 0;
        while (Empty && i < fields.length){
            fields.forEach(function(field){
                if(field.value != ""){
                    Empty = false
                }
                i++;
            })
        } 
       if(Empty){
            Swal.fire({
                type: 'info',
                text: "The form is empty",
                timer: 3000,
            });
       }
        else{
            ajaxforms('/updateProfile/' + id, 'POST', form);           
        }
    });

//Common functions  

    function ajaxforms(url, type, form){
        $.ajax({
          url: url,
          type: type,
          data: $(form).serialize(),
          cache: false,
        })
        .done(function(response){
            const callback = eval(response.callback)
            Swal.fire({
              type: response.alertType,
              text: response.message,
              timer: response.timer,
              onClose: callback
            })
          })
    }
    
    function loadProfile(){
        $('#updateProfile').load(document.URL +  '  #profileContainer ');
    }
});

