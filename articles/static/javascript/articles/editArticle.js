$(function () {
    let imagesInput = $("select#id_images").val();
    if (imagesInput) {
        setTimeout(function () {
            $.each(imagesInput,
            function (index, value) {
                addImage(value);
            })
        }, 100)
    }
    // Functions
    turn_off();
    checkFree();
    $.each($("input.toggle"), function (index, value) {
        processing_toggle($(value));
    })
    $("select#id_images").prop("required", false);
    check_messengers();
    setAvatar();
    // Handlers
    $("input.toggle#id_phone").on("change",
        function (event) {
        check_messengers();
    })
    $("input#free").on("change",
        function (event) {
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
    $("form.article-form").on("submit",
        function(event) {
        event.preventDefault();
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
            setMessage("Выберите хотя бы один из способ связи с вами",
                "red");
            return;
        }
        imagesField();
        tagsField();
        // event.preventDefault();
        // return;
        if (!$("#id_images").val()) {
            setMessage("Добавьте хотя бы одно изображение", "red");
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
    $(".image-block .fa-times").on("click", closeClick);
    $(".image-block .fa-star").on("click", starClick);
    $(".image-block .fa-plus").on("click",
        function (event) {
        $("form.image-form #id_image").click();
    });
    $("form.image-form #id_image").on("change",
        function (event) {
        $("form.image-form").submit();
    });
    $("form.image-form").on("submit",
        function (event) {
        imageRequest(event,
            function (response) {
                let color = ""
                if (response.code !== "200") {
                    color = "red";
                    setMessage(response.message, color)
                }
                if (response.code === "200") {
                    addImage(response.id);
                }
            },
            function (response) {
                setMessage("Произошла ошибка", "red")
            }
        )
    });
    $(".subject .tag.add").on("click",
        function (event) {
        getActiveTags();
        $(".classrooms").hide();
        $(".subjects").show();
        $(".popup").fadeIn();
    });
    $(".classroom .tag.add").on("click",
        function (event) {
        getActiveTags();
        $(".classrooms").show();
        $(".subjects").hide();
        $(".popup").fadeIn();
    });
    $(".popup-close").on("click",
        function (event) {
        setActiveTags();
        $(".popup").fadeOut();
    });
    $(".popup .tag").on("click",
        function (event) {
       if ($(this).hasClass("selected")) {
           $(this).removeClass("selected");
           $(this).attr("title", "Удалить тег у записи")
       }
        else {
           $(this).addClass("selected");
           $(this).attr("title", "Добавить тег к записи")
       }
    });
    $(".subject .tag:not(.add)").on("click",
        function (event) {
        $(".subject").slick("slickRemove", $(this).data("slick-index"))
    });
    $(".classroom .tag:not(.add)").on("click",
        function (event) {
        $(".classroom").slick("slickRemove", $(this).data("slick-index"))
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
function addImage(imgId) {
    let imageSlider = $(".images-slick");
    let imageId = imageSlider.slick("getSlick").slideCount - 1;
    let imageSlide = `<div class="image-wrap">
        <div class="image">
        <div class="image-block">
        <img src="/image/${imgId}" alt="" class="my-image">
        <i class="fas fa-times"></i>
        <i class="fas fa-star avatar"></i>
        </div></div></div>`;
    imageSlider.slick('slickAdd', imageSlide,
        imageId, true);
    $(`.image-wrap[data-slick-index="${imageId}"] .fa-star`).on(
        "click", starClick);
    $(`.image-wrap[data-slick-index="${imageId}"] .fa-times`).on(
        "click", closeClick);
    setAvatar();
    }
function setAvatar() {
    let avatarField = $(".article-form #id_avatar");
    let avatar = parseInt(avatarField.val());
    let wasAvatar = false;

    if (!avatar) {
        avatar = 0
        avatarField.val(avatar);
    }
    $.each($(".image-block"), function (index, value) {
       if ($(value).parent().parent().data("slick-index") === avatar) {
           $(value).children(".fa-star").addClass("avatar");
           wasAvatar = true;
       }
       else
           $(value).children(".fa-star").removeClass("avatar")
    });

    if (!wasAvatar) {
        avatarField.val("0");
        if ($(".image-block").length > 2) setAvatar();
    }
}
function imagesField() {
    let imageSelect = $("select#id_images");
    imageSelect.empty();
    $.each($(".image-block img"), function (index, value) {
        imageSelect.append(
            `<option value="${$(value).attr("src").split("/").pop()}">
            новый option</option>`)
    });
    $("select#id_images option").prop('selected', true);
}
function getActiveTags() {
    let activeSubject = $(".subject .tag:not(.add)");
    let activeClassroom = $(".classroom .tag:not(.add)");
    $(".subjects .tag").removeClass("selected");
    $(".classrooms .tag").removeClass("selected");
    $.each(activeSubject, function (index, value) {
        $(`.subjects .tag[data-tag-id="${$(value).data("tag-id")}"]`).addClass("selected");
    });
    $.each(activeClassroom, function (index, value) {
        $(`.classrooms .tag[data-tag-id="${$(value).data("tag-id")}"]`).addClass("selected");
    });
}
function setActiveTags() {
    let activeSubject = $(".popup .subjects .tag.selected");
    let activeClassroom = $(".popup .classrooms .tag.selected");
    let sliderSubject = $(".subject");
    let sliderClassroom = $(".classroom");
    $(".subject .tag:not(.add)").remove();
    $(".classroom .tag:not(.add)").remove();
    $.each(activeSubject, function (index, value) {
        sliderSubject.slick('slickAdd',
        `<span class="tag" title="Удалить тег у записи"
            data-tag-id="${$(value).data("tag-id")}">
            <i class="fas fa-times"></i>
            ${$(value).text()}
         </span>`,
        sliderSubject.slick("getSlick").slideCount - 1, true);
    })
    $.each(activeClassroom, function (index, value) {
        sliderClassroom.slick('slickAdd',
        `<span class="tag" title="Удалить тег у записи" 
            data-tag-id="${$(value).data("tag-id")}">
            <i class="fas fa-times"></i>
            ${$(value).text()}
         </span>`,
        sliderClassroom.slick("getSlick").slideCount - 1, true);
    })
}
function tagsField() {
    let tagsSelect = $("select#id_tags");
    tagsSelect.empty();
    $.each($(".subject .tag:not(.add)"), function (index, value) {
        tagsSelect.append(
            `<option value="${$(value).data("tag-id")}"></option>`)
    });
    $.each($(".classroom .tag:not(.add)"), function (index, value) {
        tagsSelect.append(
            `<option value="${$(value).data("tag-id")}"></option>`)
    });
    $("select#id_tags option").prop('selected', true);
}
function starClick(event) {
    event.preventDefault();
    console.log("star")
    let slideId = $(this).parent().parent().parent()
        .data("slick-index");
    console.log(slideId);
    $(".article-form #id_avatar").val(slideId);
    setAvatar();
}
function closeClick(event) {
    event.preventDefault();
    let delId = parseInt(
        $(this).parent().parent().parent().data("slick-index"));
    $(".images-slick").slick('slickRemove', delId);
    setAvatar();
}