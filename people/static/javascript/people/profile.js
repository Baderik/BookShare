$(function () {
    $(".fa-briefcase").on("click", function (event) {
        addNotification("Это ещё не работает. " +
            "А это значит, что скоро будет");
    });
    $(".fa-comments").on("click", function (event) {
        addNotification("Это ещё не работает. " +
            "А это значит, что скоро будет");
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
    $(".logout").on("click", function (event) {
        question = link;
        questionEvent = event;
        $(".popup").fadeIn();
    });
    $(".delete").on("click", function (event) {
        question = deleteAccount
        questionEvent = event;
        $(".popup").fadeIn();
    })
});
let answer = false;
let question = function (event) {};
let questionEvent = null;
function popupClose(event) {
    if (answer) {
        console.log(questionEvent)
        question(questionEvent);
    }
    $(".popup").fadeOut();
}
function deleteAccount() {
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