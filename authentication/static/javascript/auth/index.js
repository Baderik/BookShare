$(function () {
    $("form").on("submit", function(event) {
        setMessage("Выполняется");
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
                console.log("ajax success")
            },
            function (response) {
                setMessage("Произошла ошибка", "red")
                console.log("ajax success")
            }
            )
    });
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