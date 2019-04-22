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
   $('form#updateProfile').on('submit', function(e){
        e.preventDefault();
        const form = $(this);
        const id = form.attr('data-form-user')
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
            const data = form.serialize();
            ajaxforms('/updateProfile/' + id, 'POST', data);           
        }
    });


// Update User Avatar
$('#updateAvatar').on('submit', function(e){
    e.preventDefault();
    const form = new FormData($('#updateAvatar')[0]);    
    const id = $(this).attr('data-form-user');
    if ($(this).find('input[name="attachment"]')[0].value != ''){
        ajaxforms('/update_avatar/' + id, 'POST', form, false, false)
    }
    else{
        Swal.fire({
            type: error,
            text: 'your image must have a name',
            timer: 2500,
            onClose: $(this).reset
          })
    }
});

//Common functions
    function ajaxforms(url, type, form, pData=True, cType=True){
        $.ajax({
          url: url,
          type: type,
          data: form,
          cache: false,
          processData: pData,
          contentType: cType
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
    function loadAvatar(){
        $('#user-avatar').load(document.URL +  '  #avatar-card ');
        $('#updateAvatar').load(document.URL +  '  #btnholder ');
        $('input[name="attachment"]').val('');
        $('.thumbnail').children().remove();

    }
});

