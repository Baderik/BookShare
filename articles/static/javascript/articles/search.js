$(function () {
    $(".search-form #id_firstArticle").val(0);
    setTags();
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
    $(".search-form").on("submit", function (event) {
        tagsField();
        if (!update) $(".search-form #id_firstArticle").val(0);
        formRequest(event,
            function (response) {
                if (response.code === "200") {
                    if (!update)
                        $(".article").remove();
                    addNewArticles(response);
                }
                else
                    console.log(response.message, "red");
                if (!update)
                    $(".search-form #id_firstArticle").val(0);
                update = false;
            },
            function (response) {
                console.log("Произошла ошибка", "red");
                if (!update)
                    $(".search-form #id_firstArticle").val(0);
                update = false;
            });
    });
    $(".search-form").submit();
    $(".articles-button").on("click", function (event) {
        update = true;
        $(".search-form").submit();
    });
    $(".tags .tag").on("click",
        function (event) {
       if ($(this).hasClass("selected")) {
           $(this).removeClass("selected");
           $(this).attr("title", "Добавить тег к поиску")
       }
        else {
           $(this).addClass("selected");
           $(this).attr("title", "Удалить тег из поиска")
       }
    });
})
let update = true;
function addNewArticles(response) {
    let nextField = $(".search-form #id_firstArticle");
    if (nextField.val() === "-1") return;

    nextField.val(response.nextArticle);

    if (response.articles.length) $(".nothing").hide();
    else {
        $(".nothing").show();
        $(".articles-button").hide();
        nextField.val(-1);
        return;
    }
    $.each(response.articles, function (index, article) {
        let articleId = article.pk;
        let imageId = article.fields.images[article.fields.avatar];
        let date = new Date(
            article.fields.date).toLocaleString("ru",
            {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric'
            }).valueOf();
        let seen = article.fields.seen;
        let title = article.fields.tittle;
        let description = article.fields.description;

        let articleHtml = `
            <div class="article row no-gutters">
                <div class="col-6 image">
                    <div class="image-block">
                        <img src="/image/${imageId}" 
                        alt="" class="my-image">
                    </div>
                </div>
                <div class="col-12 col-lg-6">
                    <div class="article-block">
                        <div class="block-top">
                            <span class="date">${date}</span>
                            <span class="seen">${seen}</span>
                        </div>
                        <h3>${title}</h3>
                        <span class="desc">
                            ${description}
                        </span>
                        <button class="my-button link" 
                        data-link-href="../${articleId}">
                            Подробнее
                        </button>
                        <br>
                        <div class="image-block">
                            <img src="/image/${imageId}" 
                            alt="" class="my-image">
                        </div>
                    </div>
                </div>
            </div>`
        $(".articles .button-out").before(articleHtml)
    });
    $(".link").on("click", link)

    if (nextField.val() === "-1") $(".articles-button").hide();
    else $(".articles-button").show();
}
function setTags() {
    $(".subject .tag.active").removeClass(".selected");
    $(".classroom .tag.active").removeClass(".selected");
    $.each($("select#id_tags").val(), function (index, tagId) {
        $(`.subject .tag[data-tag-id="${tagId}"]`).addClass(
            ".selected");
        $(`.classroom .tag[data-tag-id="${tagId}"]`).addClass(
            ".selected");
    });
}
function tagsField() {
    let tagsSelect = $("select#id_tags");
    tagsSelect.empty();
    $.each($(".subject .tag.selected"), function (index, value) {
        tagsSelect.append(
            `<option value="${$(value).data("tag-id")}"></option>`)
    });
    $.each($(".classroom .tag.selected"), function (index, value) {
        tagsSelect.append(
            `<option value="${$(value).data("tag-id")}"></option>`)
    });
    $("select#id_tags option").prop('selected', true);
}