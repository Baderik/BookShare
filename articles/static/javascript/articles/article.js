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
})