

$(document).ready(function () {
    toastr.options = {
        "timeout": "3000"
    };

    // stop carousel auto play
    $('.carousel').carousel({
        interval: false
    });

    $('#btn_next_form').click(() => {
        let curIndex = $('.nav-item.active').data('number');

        curIndex++;
        if (curIndex > 5) {
            curIndex = 0;
        }

        if (curIndex === 0) {
            $('.carousel').carousel("next");
        } else {
            $('.carousel').carousel(curIndex);
        }
        $('.nav-item').removeClass("active");
        $('#item-table-' + curIndex).addClass("active");
    });

    setNavActive();
    function setNavActive() {
        var pageType = $('#my-data').data().name;
        $('#' + pageType ).addClass("active");
    }


    $('#btn_prev_form').click(() => {
        let curIndex = $('.nav-item.active').data('number');

        curIndex--;
        if (curIndex < 0) {
            curIndex = 7;
        }

        if (curIndex === 7) {
            $('.carousel').carousel("prev");
        } else {
            $('.carousel').carousel(curIndex);
        }

        $('.nav-item').removeClass("active");
        $('#item-table-' + curIndex).addClass("active");
    });

    $('.nav-item').click((event) => {
        let target = event.currentTarget;
        let number = $(target).data('number');

        $('.nav-item').removeClass("active");
        $('.carousel').carousel(number);
        $(target).addClass("active");
    });


    function createTables() {

        //$('.page-loading').fadeIn(1000);
        $.get("/create-tables", function (data) {
            //$('.page-loading').fadeOut(1000);
        });
    }

    createTables();
});

function onClear(id) {
    $('#' + id).find("input").val("");
}

function sendRequest(tablename, request, id) {
    $('.page-loading').fadeIn(1000);
    $.ajax("/add-data/" + tablename, {
        type: 'POST',
        data: request,
        success: function (data, status) {
            toastr.success("Successfully inserted");
            onClear(id);
        },
        error: function (errorMessage) {
            toastr.error("failed to insert.");
        },
        complete: function () {
            $('.page-loading').fadeOut(1000);
        }
    });
}


function onValidate(e) {
    e.preventDefault();
    let form = e.currentTarget;
    let id = $(form).attr('id');
    let formData = $(form).serializeArray();
    let tablename = "";
    if (id === 'activity_form') {
        tablename = "activity";
    } else if (id === 'client_form') {
        tablename = "client";
    } else if (id === 'insurance_form') {
        tablename = "insurance";
    } else if (id === 'provider_form') {
        tablename = "provider";
    } else if (id === 'vaccine_manufacturer_form') {
        tablename = "vaccine_manufacturer";
    } else if (id === 'student_form') {
        tablename = "student";
    }
    sendRequest(tablename, formData, id);
}

