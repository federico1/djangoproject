"use strict";

(function ($) {
    "use strict";

    $(window).scroll(function () {
        var window_top = $(window).scrollTop() + 1;

        if (window_top > 50) {
            $('.scroll-to-top').addClass('reveal');
        } else {
            $('.scroll-to-top').removeClass('reveal');
        }
    });

    // overlay search

    $('.search_toggle').on('click', function (e) {
        e.preventDefault();
        $('.search_toggle').toggleClass('active');
        $('.overlay').toggleClass('open');
        setTimeout(function () {
            $('.search-form .form-control').focus();
        }, 400);
    });


    /* ----------------------------------------------------------- */
    /*  Fixed header
    /* ----------------------------------------------------------- */

    $(window).scroll(function () {

        var window_top = $(window).scrollTop() + 1;

        // if (window_top > 50) {
        //     $('.site-navigation').addClass('menu_fixed animated fadeInDown');
        // } else {
        //     $('.site-navigation').removeClass('menu_fixed animated fadeInDown');
        // }
    });

    $.get('/api/subjects/', {}, function (response) {
     $(response).each(function(ix , item){
        var link = $("<a />", {
            class: "dropdown-item",
            href: '/course/subject/' + item.slug,
            text:item.title + " ("+item.course_count+" courses)"
        });
        $("div[aria-labelledby='navbar3']").append(link);
     });

      
    });


})(jQuery);

var ShowLoadingModal = function (title, message) {
    Swal.fire({
        title: title ? title : 'Uploading...',
        html: message ? message : 'Please wait...',
        allowEscapeKey: false,
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading()
        }
    });
};

const Toast = Swal.mixin({
    toast: true,
    position: 'top-right',
    iconColor: 'white',
    customClass: {
      popup: 'colored-toast'
    },
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true
  });
  