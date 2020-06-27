$(function () {
    $(".list-btn").click(listPressed);
    $(".link").click(link);
})
function listPressed(event) {
    if ($(this).hasClass("active")) {
        return;
    }
    let listCls = $(this).data("list-cls");
    let listId = $(this).data("list-id");

    let buttons = $(`.active[data-list-cls=${listCls}]`);
    buttons.removeClass("active")
    $(`[data-list=${buttons.data("list-id")}]`).hide();
    $(`[data-list=${listId}]`).fadeIn();
    $(this).addClass("active");
}
//Notification
function addNotification(txt){
    $(".notification").append(
        `<div class=\"notification-block\"><p>${txt}</p></div>`
    );
    let last = $(".notification-block").last();
    $(last).fadeIn();
    setTimeout(
        function(){
            $(last).fadeOut();
        },
        2000
    )
}
// Link
function link(event) {
    window.location.href = $(this).data("link-href");
}