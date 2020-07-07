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
    });
    $(".fa-comments").on("click", function (event) {
        addNotification("Это ещё не работает. А это значит, что скоро будет");
    });
    $(".fa-hands-helping").on("click", function (event) {
        addNotification("Это ещё не работает. А это значит, что скоро будет");
    });
    $(".popup-close").on("click", function (event) {
        answer = false;
        popupClose(event);
    });
    $(".popup button.no").on("click", function (event) {
        answer = false;
        popupClose(event);
    });
    $(".popup button.yes").on("click", function (event) {
        answer = true;
        popupClose(event);
    });
    $(".fa-trash-alt").on("click", function (event) {
        question = deleteArticle
        questionEvent = event;
        $(".popup").fadeIn();
    })
})
let answer = false;
let question = function (event) {};
let questionEvent = null;
function popupClose(event) {
    if (answer) {
        question(questionEvent);
    }
    $(".popup").fadeOut();
}
function deleteArticle() {
    $.ajax({
        url: "",
        method: "DELETE",
        dataType: "json",
        headers:{ "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        success: function (response) {
            if (response.code === "303")
                location.href = response.location;
            else
                alert(response.message);
        },
        error: function (response) {
            alert("Что-то пошло не так, " +
                "попробуйте позже или обратитесь в подержку")
        }
    })
}