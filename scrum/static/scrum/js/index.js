
function page_alert(message, style_class, fadeOutTime = -1) {
    $("#feedback_message").html(message);
    $("#feedback_message").removeClass();
    $("#feedback_message").addClass(style_class);
    $("#feedback_box").fadeIn('slow');

    if (fadeOutTime > 0) {
        $("#feedback_box").delay(fadeOutTime * 1000).fadeOut();
    }
}