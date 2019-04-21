$(document).ready(function() {
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
    $('.nav-mobile-menu .nav-item a.nav-link').removeClass('btn', 'btn-white', 'btn-round');
  window.onresize = navLink;
  
  function navLink(){
    if(window.innerWidth < 991){
      $('.nav-mobile-menu .nav-item a.nav-link').removeClass('btn', 'btn-white', 'btn-round');
    }
  }

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

  });
});