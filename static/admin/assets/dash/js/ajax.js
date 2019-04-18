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

