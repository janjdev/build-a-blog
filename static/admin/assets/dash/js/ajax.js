$(document).ready(function() {

//Quick Add to media library
 const quickAdd = document.getElementById('quickAdd');
 $(quickAdd).on('submit', function(e){
    e.preventDefault();
     const form = $(this);
     const formData = new FormData(form[0]);    
     if ($(this).find('input[name="attachment"]')[0].value != ''){
        ajaxforms('/admin/quickAdd', 'POST', formData,  false, false)
    }
    else{
        Swal.fire({
            type: 'error',
            text: 'your image must have a name',
            timer: 2500,
            onClose: $(this).reset
          });
    }

 })    


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
            type: 'error',
            text: 'your image must have a name',
            timer: 2500,
            onClose: $(this).reset
          })
    }
});

//Publish a new Post
const pub = document.getElementById('pubPost');
$(pub).unbind('click').click(function(e){
    e.preventDefault();
    const form = document.getElementById('newPostForm');
    const url = '/admin/posts/blog/add_post/publish';
   if(posts()){
        ajaxforms(url, 'POST', $(form).serialize(), false)
    }
    
});

//Saves Post as draft opens a new window to view the post draft
const view = document.getElementById('viewPost');
$(view).unbind('click').click(function(e){
    e.preventDefault();
})

//Post functions
function posts(){
    const title = document.getElementById('addPostTitle');
    const content = document.getElementById('contentbox');
    const titlebox = document.getElementById('titlebox');
    const postContent = document.getElementById('postcontent');
    if(title.textContent == '' || content.textContent == ''){
        Swal.fire({
            type: 'info',
            text: "You need a title and content to post",
            timer: 3000,
        });
        return false;
    }else{
        titlebox.value = $(title).html();
        postContent.value = $(content).html();
        return true;
    }
}

//Bulk Actions---------------------------------------------
const actionsSelect = document.getElementById('bulk-actions-select');
if(actionsSelect){
  actionsSelect.addEventListener('change', function(e){
    post_to_edit = [];
    for (el of document.getElementsByClassName('post-action')){
      if(el.checked == true){
        id = el.getAttribute('data-id');
        post_to_edit.push(id)
      }
    }
    if(post_to_edit.length > 0){
      let action = actionsSelect.value;
      let data = {'action': action, 'posts': post_to_edit};
      let text, type = '';

      if(action == 'Delete'){
        text = 'You are going to '+action+' '+post_to_edit.length+' post(s). They will be permanently lost. Cause implementing a trashcan feature is not on my list.' ;
        type = 'warning';
      }else{
          text = 'You are going to '+action+' '+post_to_edit.length+' post(s).';
          type='question';
      }
      Swal.fire({
        title: 'Really ?',
        text: text,
        type: type,
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes',
      }).then((result) =>{
            if(result.value){
                ajax('/admin/posts/bulk_action', 'POST', data, false)
                }
            });
        }
    });
  }


//Common functions
    function ajaxforms(url, type, form, pData=true, cType='application/x-www-form-urlencoded; charset=UTF-8', dType='', convert=false){
        $.ajax({
          url: url,
          type: type,
          data: form,
          cache: false,
          processData: pData,
          contentType: cType,
          dataType: dType,
        //   converters: {
        //     'text json': convert
        //   }
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
    
    function loadProfile(){
        $('#updateProfile').load(document.URL +  '  #profileContainer ');
    }
    function loadAvatar(){
        $('#user-avatar').load(location.href +  '  #avatar-card ');
        $('.fileinput.text-center').removeClass('fileinput-exists');
        $('.fileinput.text-center').addClass('fileinput-new');
        $('.thumbnail').children().remove();
    }
    function openView(url){

      setTimeout(() => {
        window.open(url, '_blank');
      }, 3000);

       
    }
    function reset(el){
        el.reset;
        $('.fileinput.text-center').removeClass('fileinput-exists');
        $('.fileinput.text-center').addClass('fileinput-new');
    }
});

