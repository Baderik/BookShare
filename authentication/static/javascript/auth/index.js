$(function () {
    $("form").on("submit", function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            method: $(this).attr("method"),
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                let color = ""
                if (response.code !== "303" && response.code !== "200") {
                    color = "red";
                }
                setMessage(response.message, color)
                if (response.code === "303") {
                    location.href = response.location;
                }
            },
            error: function (response) {
                setMessage("Произошла ошибка", "red")
            }
        })
    })
})
function setMessage(text, color) {
    let message = $(".pre-auth span");
    let spanMessage = $(".blur .message");
    message.text(text);
    spanMessage.html(text + "<br><br>")
    if (color) {
        message.css("text-shadow", `0 0 0.2rem ${color}`);
        spanMessage.css("text-shadow", `0 0 0.2rem ${color}`);
    }
}