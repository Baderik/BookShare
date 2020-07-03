$(function () {
    // setWidthHeightImg();
    // Handlers
    $(".list-btn").click(listPressed);
    $(".link").click(link);
    // Copy text
    $(".copy").on("click", function (event) {
        event.preventDefault();
        copyText($(this).data("copy-el"), $(this).data("format"));
        addNotification("Скопированно в буфер обмена");
    });
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
// FormSendler
function formRequest(event, success=function (response) {},
                     error=function (response) {}) {
    event.preventDefault();
    $.ajax({
        url: $(event.currentTarget).attr("action"),
        method: $(event.currentTarget).attr("method"),
        data: $(event.currentTarget).serialize(),
        dataType: "json",
        success: success,
        error: error
    })
}
function imageRequest(event, success=function (response) {},
                     error=function (response) {}) {
    event.preventDefault();
    $.ajax({
        url: $(event.currentTarget).attr("action"),
        method: $(event.currentTarget).attr("method"),
        data: new FormData($(event.currentTarget).get(0)),
        dataType: "json",
        processData: false,
        contentType: false,
        success: success,
        error: error
    })
}
// Copy
function copyText(el, format=false) {
    if (format){
        let $temp = $("<div>");
        $("body").prepend($temp);
        $temp.attr("contenteditable", true)
           .html($(el).html()).select()
           .on("focus", function() { document.execCommand('selectAll',false,null); })
           .focus();
        document.execCommand("copy");
        $temp.remove();
    }
    else {
        let $tmp = $("<textarea>");
        $("body").append($tmp);
        $tmp.val($(el).text()).select();
        document.execCommand("copy");
        $tmp.remove();
    }
}
// Width and height img
function calcMaxSize(max, parentValue) {
    if (max.slice(-1) === "%") {
        max = parseInt(max);
        return  parseInt(parentValue) * max / 100;
    }
    return parseInt(max);
}

function setWidthHeightImg(image=".image-wh") {
    let images = $(image);
    $.each(images, function (index, value) {
        let parent = $(value).parent();

        $(value).removeAttr("width")
            .removeAttr("height")

        let width  = parseInt($(value).width());
        let height = parseInt($(value).height());
        console.log(value)
        console.log(width, height)
        let maxWidth = calcMaxSize(
            $(value).data("image-wh-width"), parent.width());
        let maxHeight = calcMaxSize(
            $(value).data("image-wh-height"), parent.height());

        let proportion = width / height;

        if (proportion < maxWidth / maxHeight) {
            height = maxHeight;
            width = proportion * height;
        }
        else {
            width = maxWidth;
            height = width / proportion;
        }

        $(value).width(width);
        $(value).height(height);
    })
}
