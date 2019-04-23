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
        $('#user-avatar').load(location.href +  '  #avatar-card ');
        $('.fileinput.text-center').removeClass('fileinput-exists');
        $('.fileinput.text-center').addClass('fileinput-new');
        $('.thumbnail').children().remove();
    }
});

