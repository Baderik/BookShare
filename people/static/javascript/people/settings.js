$(function(){
    setAvatar();
    $("form.image-form #id_image").attr("id", "image");
    $("#id_phone").mask("+7 (000) 000-00-00");
    $("form.profile-block").on("submit", function(event) {
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
                if (response.code === "200") {
                    $(".email .accept").hide();
                    $(".email .times").hide();
                    $(".email .edit").hide();
                    emailBase = $(".email input").val();
                    emailAccept = response.email;
                    if (emailAccept) $(".email .accept").show();
                    else $(".email .times").show();
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
            else $(".email .times").show();
        }
   });
    $("form.image-form").on("submit", function (event) {
        imageRequest(event,
            function (response) {
                let color = ""
                if (response.code !== "200") {
                    color = "red";
                    setMessage(response.message, color)
                }
                if (response.code === "200") {
                    $(".profile-block #id_image").val(response.id);
                    setAvatar();
                }
            },
            function (response) {
                setMessage("Произошла ошибка", "red")
            }
        )
    });
    $(".image-block img").on("click", function (event) {
        $("form.image-form input").click();
    });
    $("form.image-form #image").on("change", function (event) {
        $("form.image-form").submit();
    });
    $(".fa-times").on("click", function (event) {
        $(".profile-block #id_image").val("");
        setAvatar();
    });
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

function setAvatar() {
    let avatar = $(".profile-block #id_image").val();
    if (avatar) {
        $(".main-img img").attr("src",
            `/image/${avatar}`);
        $(".image-block img").attr("src",
            `/image/${avatar}`);
        $(".fa-times").show();
    }
    else {
        $(".main-img img").attr("src",
            avatarBase);
        $(".image-block img").attr("src",
            avatarBase);
        $(".fa-times").hide();
    }
}