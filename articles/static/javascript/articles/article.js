$(function () {
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

    if ($("#id_cost").val() === "0") {
        $("#id_cost").val("Бесплатно")
        $(".currency").hide();
    }

    $(".messenger").on("click", function (event) {
        addNotification("По номеру телефона, пожалуйста");
    })
    $(".fa-comments").on("click", function (event) {
        addNotification("Это ещё не работает. А это значит, что скоро будет");
    })
    $(".fa-hands-helping").on("click", function (event) {
        addNotification("Это ещё не работает. А это значит, что скоро будет");
    })
})