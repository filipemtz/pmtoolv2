
function show_user_notes_editor() {
    $.ajax({
        method: "GET",
        url: "/scrum/user_note",
        mode: 'same-origin', // Do not send CSRF token to another domain.
    }).done(function (data) {
        // refactor the modal name
        $("#details-form-placeholder").html(data);
        $("#user_note_textarea").focus();
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    })
}


function save_user_note(note_id) {
    $.ajax({
        method: "POST",
        url: "/scrum/user_note/update/" + note_id,
        mode: 'same-origin', // Do not send CSRF token to another domain.
        data: {
            'content': $("#user_note_textarea").val(),
        }
    }).done(function (data) {
        page_alert('saved', SUCCESS_CLASS, fadeOutTime = 0.5);
    }).fail(function (data) {
        page_alert('fail', FAIL_CLASS, fadeOutTime = 1);
    })
}
