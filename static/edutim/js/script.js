"use strict";

(function ($) {
    "use strict";

    var subjestList = [];

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

    countdownTimeStart();

    $.get('/api/subjects/', {}, function (response) {
        renderTopSubjects(response);
        subjestList = response;
    });

    $("#txtSearchSubjects").keyup(function (e) {

        var val = $.trim($(this).val());

        if (val) {
            var filter = subjestList.filter(a => a.title.toLowerCase().indexOf(val) >= 0);
            renderTopSubjects(filter);
        }
        else {
            renderTopSubjects(subjestList);
        }

    });

    $("#btnClearSubjectSearch").click(function (e) {

        $("#txtSearchSubjects").val(null);

        renderTopSubjects(subjestList);

    });

    function renderTopSubjects(dataList) {
        $("div[aria-labelledby='navbar3'] #listItems").empty();
        $(dataList).each(function (ix, item) {
            var link = $("<a />", {
                class: "dropdown-item",
                href: '/course/subject/' + item.slug + '/',
                text: item.title + " (" + item.course_count + " courses)"
            });
            $("div[aria-labelledby='navbar3'] #listItems").append(link);
        });
    };

    function countdownTimeStart() {

        var countDownDate = new Date('April 2, 2024 24:00:00').getTime();

        // Update the count down every 1 second
        var x = setInterval(function () {

            // Get todays date and time
            var now = new Date().getTime();

            // Find the distance between now an the count down date
            var distance = countDownDate - now;

            // Time calculations for days, hours, minutes and seconds
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Output the result in an element with id="demo"
            document.getElementById("disountTime").innerHTML = hours + "h "
                + minutes + "m " + seconds + "s ";

            if (distance < 0) {
                clearInterval(x);
                $("#discountHeader").remove();
            }

        }, 1000);
    }

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
