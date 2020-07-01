$(function () {
    // Functions
    turn_off();
    checkFree();
    $.each($("input.toggle"), function (index, value) {
        processing_toggle($(value));
    })
    check_messengers();
    // Handlers
    $("input.toggle#id_phone").on("change", function (event) {
        check_messengers();
    })
    $("input#free").on("change", function (event) {
        checkFree();
    })
    $(".subject").slick({
        dots: false,
        infinite: false,
        speed: 300,
        slidesToShow: 1,
        variableWidth: true,
        adaptiveHeight: true
    });
    $(".classroom").slick({
        dots: false,
        infinite: false,
        speed: 300,
        slidesToShow: 1,
        variableWidth: true,
        adaptiveHeight: true
    });
    $(".images-slick").slick({
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 1,
        variableWidth: true,
        adaptiveHeight: true
    });
    $("form").on("submit", function(event) {
        $("input.toggle").prop("disabled", false);
        $("input.toggle#free").prop("disabled", true);

        let author = false;

        $.each($("input.toggle:not([id=free])"), function (index, value) {
            if ($(value).is(":checked")) {
                author = true;
                return false;
            }
        })

        if (!author) {
            event.preventDefault();
            setMessage("Выберите хотя бы один сз способ связи с вами", "red");
            return;
        }
        formRequest(event,
            function (response) {
                let color = ""
                if (response.code !== "303" && response.code !== "200") {
                    color = "red";
                }
                setMessage(response.message, color)
                if (response.code === "303") {
                    location.href = response.location;
                }
            },
            function (response) {
                setMessage("Произошла ошибка", "red")
            }
            )
    });
})

function checkFree() {
    let input = $("input#id_price");
    let rub = $('span.currency');

    if ($("input#free").is(":checked")) {
        input.val(0);
        $(input).fadeOut();
        $(rub).fadeOut();
    }
    else {
        $(input).fadeIn();
        $(rub).fadeIn();
    }
}

function processing_toggle(toggle) {
    let myToggle = toggle.parent();
    let blockToggle = myToggle.parent();
    let spanToggle = myToggle.siblings("span:first");

    if (toggle.prop("disabled")){
        spanToggle.addClass("disabled");
        blockToggle.attr("title", toggle.data("disabled-title"));
    }
    else {
        spanToggle.removeClass("disabled");
        blockToggle.removeAttr("title");
    }

}

function check_messengers() {
    let telegram = $("input.toggle#id_telegram");
    let whatsApp = $("input.toggle#id_whatsapp");
    let viber = $("input.toggle#id_viber");

    if ($("input.toggle#id_phone").is(":checked")) {
        if (telegram.prop("disabled"))
            telegram.prop("disabled", false);
        if (whatsApp.prop("disabled"))
            whatsApp.prop("disabled", false);
        if (viber.prop("disabled"))
            viber.prop("disabled", false);
    }
    else {
        telegram.prop("disabled", true);
        whatsApp.prop("disabled", true);
        viber.prop("disabled", true);
    }
    processing_toggle(telegram);
    processing_toggle(whatsApp);
    processing_toggle(viber);
}

function turn_off() {
    let elements = [
        ["#id_phone", phone],
        ["#id_vk", vk],
        ["#id_facebook", facebook],
        ["#id_twitter", twitter],
        ["#id_odnoklassniki", odnoklassniki],
    ];

    $.each(elements, function (index, value) {
        if (value[1]) $(value[0]).prop("disabled", false);
        else $(value[0]).prop("disabled", true);
    })
}

function setMessage(text, color) {
    let message = $(".message span");
    message.text(text);
    if (color) {
        message.css("text-shadow", `0 0 0.2rem ${color}`);
    }
    let top = $('header').offset().top;
    $(".message").fadeIn();
    $('html').animate({ "scrollTop": top }, "1100");
}