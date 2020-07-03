$(function () {
    // Functions
    turn_off();
    checkFree();
    $.each($("input.toggle"), function (index, value) {
        processing_toggle($(value));
    })
    check_messengers();
    setAvatar();
    // Handlers
    $("input.toggle#id_phone").on("change",
        function (event) {
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
    $("form.article-form").on("submit", function(event) {
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
    $(".image-block .fa-times").on("click", function (event) {
        event.preventDefault();
        let delId = parseInt($(this).parent().data("slick-slide"));
        $(".images-slick").slick('slickRemove',
            $(this).parent().data("slick-slide"));
        $.each($(".image-block .fa-times"),
            function (index, value) {
            let slideId = parseInt($(value).parent().data("slick-slide"));

            if (delId < slideId) {
                $(value).parent().data("slick-slide", slideId - 1);
                if ($(value).siblings(".fa-star")
                    .hasClass("avatar")) {
                    $(".article-form #id_avatar").val(
                        slideId - 1
                    );
                }
            }
        });
        setAvatar();
    })
    $(".image-block .fa-star").on("click", function (event) {
        event.preventDefault();
        let slideId = $(this).parent().data("slick-slide");
        $(".article-form #id_avatar").val(slideId);
        setAvatar();
    })
    $(".image-block .fa-plus").on("click", function (event) {

    })
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


function setAvatar() {
    let avatar = parseInt($(".article-form #id_avatar").val());
    let wasAvatar = false;

    if (!avatar) {
        avatar = 0
        $(".article-form #id_avatar").val(avatar);
    }
    $.each($(".image-block"), function (index, value) {
       if ($(value).data("slick-slide") === avatar) {
           $(value).children(".fa-star").addClass("avatar");
           wasAvatar = true;
       }
       else
           $(value).children(".fa-star").removeClass("avatar")
    });

    if (!wasAvatar) {
        $(".article-form #id_avatar").val("0");
        if ($(".image-block").length < 2) setAvatar();
    }
}