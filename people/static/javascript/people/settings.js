$(function(){
    let emailBase = $(".email input").val();

    $("#id_phone").mask("+7 (000) 000-00-00");
    $("form").on("submit", function(event) {
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
    $(".email input").on("keyup", function (event) {
        $(".email .accept").hide();
        $(".email .times").hide();
        $(".email .edit").hide();
        if ($(".email input").val() != emailBase) $(".email .edit").show();
        else {
            if (emailAccept) $(".email .accept").show();
            else $(".email .times").hide();
        }
   })
});

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