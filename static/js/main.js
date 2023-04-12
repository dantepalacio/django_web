function likeArticle(articleId, currentStatus) {
    $.ajax({
        type: "POST",
        url: "/like_article/",
        data: {
            article_id: articleId,
            current_status: currentStatus,
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        success: function(newStatus) {
            var icon = $("#like-icon-" + articleId);
            if (newStatus === "liked") {
                icon.removeClass("fa-thumbs-up blue");
                icon.addClass("fa-thumbs-up black");
            } else {
                icon.removeClass("fa-thumbs-up black");
                icon.addClass("fa-thumbs-up blue");
            }
        }
    });
}